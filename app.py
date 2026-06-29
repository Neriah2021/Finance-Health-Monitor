import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import anthropic
import os
from dotenv import load_dotenv
from data_fetcher import fetch_and_store
from analysis import compute_metrics

import os
load_dotenv('config.env')
api_key = os.getenv('ANTHROPIC_API_KEY') or st.secrets.get('ANTHROPIC_API_KEY')
client = anthropic.Anthropic(api_key=api_key)

def generate_narrative(ticker, metrics):
    latest = metrics.iloc[-1]
    prev = metrics.iloc[-2]
    prompt = f'You are a CFO analyst. Write a concise 3-paragraph financial summary for {ticker} based on this data: Revenue ${latest["revenue"]/1e9:.1f}B growing at {latest["revenue_growth"]:.1f}% YoY. Gross margin {latest["gross_margin"]:.1f}% (vs {prev["gross_margin"]:.1f}% prior year). Operating margin {latest["operating_margin"]:.1f}% (vs {prev["operating_margin"]:.1f}% prior year). Net margin {latest["net_margin"]:.1f}%. Be direct and analytical. No bullet points.'
    message = client.messages.create(model='claude-sonnet-4-6', max_tokens=500, messages=[{'role': 'user', 'content': prompt}])
    return message.content[0].text

st.set_page_config(page_title='Company Financial Health Monitor', layout='wide')
st.title('Company Financial Health Monitor')

ticker = st.text_input('Enter a stock ticker', value='MSFT').upper()

if st.button('Analyse'):
    with st.spinner('Fetching data...'):
        fetch_and_store(ticker)
    metrics = compute_metrics(ticker)
    st.markdown(f'**{ticker}** - 4-Year Financial Performance Summary')
    st.divider()
    latest = metrics.iloc[-1]
    prev = metrics.iloc[-2]
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric('Revenue (Latest)', f'${latest["revenue"]/1e9:.1f}B', delta=f'{latest["revenue_growth"]:.1f}% YoY')
    with col2:
        st.metric('Gross Margin', f'{latest["gross_margin"]:.1f}%', delta=f'{(latest["gross_margin"]-prev["gross_margin"]):.1f}pp')
    with col3:
        st.metric('Operating Margin', f'{latest["operating_margin"]:.1f}%', delta=f'{(latest["operating_margin"]-prev["operating_margin"]):.1f}pp')
    with col4:
        st.metric('Net Margin', f'{latest["net_margin"]:.1f}%', delta=f'{(latest["net_margin"]-prev["net_margin"]):.1f}pp')
    st.divider()
    col_left, col_right = st.columns(2)
    with col_left:
        st.subheader('Revenue Growth ($B)')
        fig1 = px.bar(metrics, x='date', y='revenue', text=metrics['revenue'].apply(lambda x: f'${x/1e9:.0f}B'), color_discrete_sequence=['#0078D4'])
        fig1.update_traces(textposition='outside')
        fig1.update_layout(xaxis_title='Year', yaxis_title='Revenue ($)', showlegend=False, xaxis=dict(type='category'))
        st.plotly_chart(fig1, use_container_width=True)
    with col_right:
        st.subheader('Margin Trends (%)')
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(x=metrics['date'], y=metrics['gross_margin'], mode='lines+markers', name='Gross Margin', line=dict(color='#0078D4', width=2)))
        fig2.add_trace(go.Scatter(x=metrics['date'], y=metrics['operating_margin'], mode='lines+markers', name='Operating Margin', line=dict(color='#00B294', width=2)))
        fig2.add_trace(go.Scatter(x=metrics['date'], y=metrics['net_margin'], mode='lines+markers', name='Net Margin', line=dict(color='#FFB900', width=2)))
        fig2.update_layout(xaxis_title='Year', yaxis_title='Margin (%)', xaxis=dict(type='category'))
        st.plotly_chart(fig2, use_container_width=True)
    st.divider()
    st.subheader('Full Metrics Table')
    display = metrics[['date', 'revenue', 'gross_margin', 'operating_margin', 'net_margin', 'revenue_growth']].copy()
    display['revenue'] = display['revenue'].apply(lambda x: f'${x/1e9:.1f}B')
    display['gross_margin'] = display['gross_margin'].apply(lambda x: f'{x:.1f}%')
    display['operating_margin'] = display['operating_margin'].apply(lambda x: f'{x:.1f}%')
    display['net_margin'] = display['net_margin'].apply(lambda x: f'{x:.1f}%')
    display['revenue_growth'] = display['revenue_growth'].apply(lambda x: f'{x:.1f}%' if pd.notna(x) else '-')
    display.columns = ['Year', 'Revenue', 'Gross Margin', 'Operating Margin', 'Net Margin', 'Revenue Growth']
    st.dataframe(display, use_container_width=True, hide_index=True)
    st.divider()
    st.subheader('AI Financial Narrative')
    with st.spinner('Generating CFO summary...'):
        narrative = generate_narrative(ticker, metrics)
    st.write(narrative)
