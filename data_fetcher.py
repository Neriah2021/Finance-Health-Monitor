import yfinance as yf
import pandas as pd
import sqlite3
import os

DB_NAME = "financial_data.db"

def fetch_and_store(ticker="MSFT"):
    print(f"Fetching financial data for {ticker}...")
    stock = yf.Ticker(ticker)

    # Income statement
    income = stock.financials.T.reset_index()
    income.rename(columns={"index": "date"}, inplace=True)
    income["ticker"] = ticker

    # Balance sheet
    balance = stock.balance_sheet.T.reset_index()
    balance.rename(columns={"index": "date"}, inplace=True)
    balance["ticker"] = ticker

    # Cash flow
    cashflow = stock.cashflow.T.reset_index()
    cashflow.rename(columns={"index": "date"}, inplace=True)
    cashflow["ticker"] = ticker

    # Store in SQLite
    conn = sqlite3.connect(DB_NAME)
    income.to_sql("income_statement", conn, if_exists="replace", index=False)
    balance.to_sql("balance_sheet", conn, if_exists="replace", index=False)
    cashflow.to_sql("cash_flow", conn, if_exists="replace", index=False)
    conn.close()

    print(f"Data saved to {DB_NAME}")
    print(f"Income statement rows: {len(income)}")

if __name__ == "__main__":
    fetch_and_store()