import pandas as pd
import datetime

def process(path_to_csv_file_1, path_to_csv_file_2):
    # Method Chain 1: load and process data for merging
    stocks_df = (
        pd.read_csv(path_to_csv_file_1)
        .rename(columns={'Adj Close': 'Adj_Close'})
        .assign(Date=pd.to_datetime(pd.read_csv(path_to_csv_file_1)['Date']))
    )
    
    # Method Chain 2: load and process data for merging
    iPhone_df = (
        pd.read_csv(path_to_csv_file_2)
        .assign(Release_Date=pd.to_datetime(pd.read_csv(path_to_csv_file_2)['Release_Date']))
    )
    
    # Method Chain 3: merge the two dataframes
    df = (
        pd.merge(stocks_df, iPhone_df, how='outer', left_on='Date', right_on='Release_Date')
        .dropna(subset=['Adj_Close'])
    )
    
    # Method Chain 4: create new columns, drop unneeded columns, and drop unneeded rows
    cutoff_date = pd.to_datetime('2000-01-01')
    df = (
        df.assign(Change = df['Close'] - df['Open'])
        .drop(columns=['Close', 'Open', 'Release_Date', 'High', 'Low', 'Volume'])
        .loc[df['Date'] >= cutoff_date]
    )
    return df






