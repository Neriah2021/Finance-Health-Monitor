# Company Financial Health Monitor

An AI-powered financial analysis dashboard that pulls real financial data for any public company, computes key performance metrics using SQL, and generates a CFO-style narrative summary using the Claude API.

**Live app:** https://finance-health-monitor-fzreuptdmsmrrh4fraq3he.streamlit.app/

---

## What it does

Enter any stock ticker (e.g. MSFT, AAPL, GOOGL) and the app will:

- Fetch 4 years of income statement data from Yahoo Finance
- Store it in a local SQLite database
- Compute revenue growth, gross margin, operating margin, and net margin using SQL queries
- Display KPI cards, revenue bar chart, and margin trend lines in an interactive Streamlit dashboard
- Generate a 3-paragraph CFO-style financial narrative using the Anthropic Claude API

---

## Skills demonstrated

- Python (pandas, yfinance, streamlit, anthropic, plotly)
- SQL (SQLite queries for financial metric computation)
- Data pipeline (API ingestion to database to dashboard)
- AI tool fluency (Claude API for automated financial narrative generation)
- Streamlit (deployed interactive web application)

---

## Tech stack

- Python 3.14
- yfinance (financial data)
- SQLite (local database)
- Streamlit (dashboard)
- Plotly (charts)
- Anthropic Claude API (AI narrative)

---

## How to run locally

1. Clone the repository
2. Install dependencies: pip install -r requirements.txt
3. Add your Anthropic API key to a config.env file: ANTHROPIC_API_KEY=your-key-here
4. Run: streamlit run app.py

---

## Project context

Built as part of a Finance Data Engineer portfolio targeting roles at Anthropic, Snowflake, Google, and SumUp. The project demonstrates the ability to build end-to-end data pipelines that combine financial domain knowledge with modern data engineering tools and AI-powered automation.
