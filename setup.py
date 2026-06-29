analysis_code = [
    "import sqlite3\n",
    "import pandas as pd\n",
    "\n",
    "DB_NAME = 'financial_data.db'\n",
    "\n",
    "def get_income_statement(ticker='MSFT'):\n",
    "    conn = sqlite3.connect(DB_NAME)\n",
    "    df = pd.read_sql('SELECT * FROM income_statement WHERE ticker = ?', conn, params=(ticker,))\n",
    "    conn.close()\n",
    "    return df\n",
    "\n",
    "def compute_metrics(ticker='MSFT'):\n",
    "    df = get_income_statement(ticker)\n",
    "    df['date'] = pd.to_datetime(df['date'])\n",
    "    df = df.sort_values('date')\n",
    "    metrics = pd.DataFrame()\n",
    "    metrics['date'] = df['date'].dt.year.astype(str)\n",
    "    metrics['revenue'] = df['Total Revenue'].values\n",
    "    metrics['gross_profit'] = df['Gross Profit'].values\n",
    "    metrics['operating_income'] = df['Operating Income'].values\n",
    "    metrics['net_income'] = df['Net Income'].values\n",
    "    metrics['gross_margin'] = (metrics['gross_profit'] / metrics['revenue'] * 100).round(2)\n",
    "    metrics['operating_margin'] = (metrics['operating_income'] / metrics['revenue'] * 100).round(2)\n",
    "    metrics['net_margin'] = (metrics['net_income'] / metrics['revenue'] * 100).round(2)\n",
    "    metrics['revenue_growth'] = (metrics['revenue'].pct_change() * 100).round(2)\n",
    "    return metrics\n",
]

with open('analysis.py', 'w', encoding='utf-8') as f:
    f.writelines(analysis_code)

print('analysis.py created successfully')