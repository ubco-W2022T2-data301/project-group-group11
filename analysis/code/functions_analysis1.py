import pandas as pd
import datetime

def process(path_to_csv_file_1, path_to_csv_file_2):
    # Method Chain 1: load data, rename columns, convert Date to a datetime object, remove unneeded rows and columns.
    stocks_df = (
        pd.read_csv(path_to_csv_file_1)
        .rename(columns={'Adj Close': 'Adj_Close'})
        .assign(Date=pd.to_datetime(pd.read_csv(path_to_csv_file_1)['Date']))
        .loc[lambda x: x['Date'] >= pd.to_datetime('2000-01-01')]
    )
    
    # Method Chain 2: load data and convert Release_Date to a datetime object for merging
    iPhone_df = (
        pd.read_csv(path_to_csv_file_2)
        .assign(Release_Date=pd.to_datetime(pd.read_csv(path_to_csv_file_2)['Release_Date']))
    )
    
    # Method Chain 3: merge the two dataframes, drop the extra date column, and remove rows without dates
    df = (
        pd.merge(stocks_df, iPhone_df, how='outer', left_on='Date', right_on='Release_Date')
        .drop(columns=['Release_Date'])
        .dropna(subset=['Date'])
    )
    # Method Chain 4: creating new columns and dropping unneeded columns
    df = (
        df
        .assign(Two_Week_Difference = lambda x: x['Adj_Close'].shift(14).rolling(14).mean() - x['Adj_Close'].rolling(14).mean())
        .assign(Percent_Change = lambda x: x['Two_Week_Difference'] / x['Adj_Close'].iloc[0] * 100)
        .assign(Year = lambda x: x['Date'].dt.year)
        .assign(Beginning_Of_Year = lambda x: x.groupby('Year')['Adj_Close'].transform('first'))
        .assign(Percent_Change = lambda x: x['Two_Week_Difference'] / x['Beginning_Of_Year'] * 100)
        .drop(columns=['Close', 'Open', 'High', 'Low', 'Volume', 'Year', 'Beginning_Of_Year'])
    )
    return df






