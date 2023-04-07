import pandas as pd
import datetime

def process_data(df1_csv, df2_csv):
    #AAPL_df and MSFT_df methods chains: load data, drop unnecessary columns, create percent, changes, create 30 day moves, clear rows with nan values, drop excess columns, format date
    #merged df: merges all data from AAPL_df and MSFT_df to be used in visualizations.
    
    AAPL_df = (
        pd.read_csv(df1_csv)
        .drop(columns=['Adj Close', 'Volume', 'High', 'Low'])
        .assign(pct_change = lambda x: x[['Open', 'Close']].pct_change(axis=1)['Close'])
        .loc[:,['Date','Open','Close','pct_change']]
        .assign(D30_move = lambda x: x['Close'].rolling(window=30).mean())
        .assign(D30_pct_chg = lambda x: x['pct_change'].rolling(window=30).mean())
        .iloc[29:]
        .drop(columns=['Open', 'Close', 'pct_change'])
    )
    
    MSFT_df = (
        pd.read_csv(df2_csv)
        .drop(columns=['Adj Close', 'Volume', 'High', 'Low'])
        .assign(pct_change = lambda x: x[['Open', 'Close']].pct_change(axis=1)['Close'])
        .loc[:,['Date','Open','Close','pct_change']]
        .assign(D30_move = lambda x: x['Close'].rolling(window=30).mean())
        .assign(D30_pct_chg = lambda x: x['pct_change'].rolling(window=30).mean())
        .iloc[29:]
        .drop(columns=['Open', 'Close', 'pct_change'])
    )
    
    merged = pd.merge(AAPL_df, MSFT_df, on='Date', suffixes=('_AAPL', '_MSFT'))

    return merged
                                                                        
def compare_data(df):
    
    growth_df = (
        pd.DataFrame(0, index=df.index, columns=['AAPL_faster', 'MSFT_faster'])
        .assign(Year = df['Date'].dt.year)
    )
    
    for i in range(len(df)):
        if df['D30_pct_chg_AAPL'][i] > df['D30_pct_chg_MSFT'][i]:
            growth_df['AAPL_faster'][i] += 1
        elif df['D30_pct_chg_MSFT'][i] > df['D30_pct_chg_AAPL'][i]:
            growth_df['MSFT_faster'][i] += 1
    
    return growth_df.groupby('Year').sum()
                                                                        