import streamlit as st
import pandas as pd
from typing import Dict

def render_stock_info(stock_info: Dict):
    """Render stock information in a clean format"""
    st.subheader("Stock Information")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Current Price", f"₽{stock_info.get('PREVPRICE', 'N/A')}")
        st.metric("Lot Size", stock_info.get('LOTSIZE', 'N/A'))
        
    with col2:
        st.metric("Volume", f"₽{stock_info.get('VALTODAY', 'N/A'):,.2f}")
        st.metric("Face Value", f"₽{stock_info.get('FACEVALUE', 'N/A')}")

def render_stock_selector(stocks: pd.DataFrame):
    """Render the stock selector widget"""
    st.sidebar.header("Select Stock")
    
    # Create a formatted display for each stock
    stock_options = stocks.apply(
        lambda x: f"{x['SECID']} - {x['SHORTNAME']}", 
        axis=1
    ).tolist()
    
    selected_stock = st.sidebar.selectbox(
        "Choose a stock from top 30",
        options=stock_options,
        index=0
    )
    
    # Extract ticker from selection
    return selected_stock.split(" - ")[0]

def render_time_period_selector():
    """Render the time period selector"""
    return st.sidebar.slider(
        "Select Time Period (Days)",
        min_value=7,
        max_value=365,
        value=30,
        step=7
    )
