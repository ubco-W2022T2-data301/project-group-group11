import pandas as pd
import datetime

def process(path_to_csv_file_1, path_to_csv_file_2):
    # Method Chain 1: load data, rename columns, convert Date to a datetime object, create the difference column, remove unneeded rows and columns.
    stocks_df = (
        pd.read_csv(path_to_csv_file_1)
        .rename(columns={'Adj Close': 'Adj_Close'})
        .assign(Date=pd.to_datetime(pd.read_csv(path_to_csv_file_1)['Date']))
        .assign(Change = lambda x: x['Close'] - x['Open'])
        .assign(One_Week_Difference = lambda x: x['Adj_Close'].shift(7).rolling(7).mean() - x['Adj_Close'].rolling(7).mean())
        .loc[lambda x: x['Date'] >= pd.to_datetime('2000-01-01')]
        .drop(columns=['Close', 'Open', 'High', 'Low', 'Volume'])
    )
    
    # Method Chain 2: load data and convert Release_Date to a datetime object for merging
    iPhone_df = (
        pd.read_csv(path_to_csv_file_2)
        .assign(Release_Date=pd.to_datetime(pd.read_csv(path_to_csv_file_2)['Release_Date']))
    )
    
    # Method Chain 3: merge the two dataframes and drop the extra date column
    df = (
        pd.merge(stocks_df, iPhone_df, how='outer', left_on='Date', right_on='Release_Date')
        .drop(columns=['Release_Date'])
        .dropna(subset=['Date'])
    )

    return df






