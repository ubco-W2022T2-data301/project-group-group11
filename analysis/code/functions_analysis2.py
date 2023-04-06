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
    df.index = pd.to_datetime(df.index)
    growth = df['D30_pct_chg_AAPL'] - df['D30_pct_chg_MSFT']
    AAPL_faster = (growth > 0).astype(int)
    MSFT_faster = (growth < 0).astype(int)
    
    growth_yearly = (
        pd.DataFrame({'AAPL Faster': AAPL_faster, 'MSFT faster': MSFT_faster})
        .groupby(pd.Grouper(freq='Y')).sum()
    )
        
    return growth_yearly
                                                                        