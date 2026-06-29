import sqlite3
import pandas as pd

DB_NAME = 'financial_data.db'

def get_income_statement(ticker='MSFT'):
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql('SELECT * FROM income_statement WHERE ticker = ?', conn, params=(ticker,))
    conn.close()
    return df

def compute_metrics(ticker='MSFT'):
    df = get_income_statement(ticker)
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values('date')
    df = df.dropna(subset=['Total Revenue'])
    metrics = pd.DataFrame()
    metrics['date'] = df['date'].dt.year.astype(str)
    metrics['revenue'] = df['Total Revenue'].values
    metrics['gross_profit'] = df['Gross Profit'].values
    metrics['operating_income'] = df['Operating Income'].values
    metrics['net_income'] = df['Net Income'].values
    metrics['gross_margin'] = (metrics['gross_profit'] / metrics['revenue'] * 100).round(2)
    metrics['operating_margin'] = (metrics['operating_income'] / metrics['revenue'] * 100).round(2)
    metrics['net_margin'] = (metrics['net_income'] / metrics['revenue'] * 100).round(2)
    metrics['revenue_growth'] = (metrics['revenue'].pct_change() * 100).round(2)
    metrics = metrics.dropna(subset=['revenue'])
    return metrics
