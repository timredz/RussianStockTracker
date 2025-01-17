import streamlit as st
import pandas as pd
from api_client import MOEXClient
from utils import create_candlestick_chart, format_stock_info
from components import render_stock_info, render_stock_selector, render_time_period_selector

# Page configuration
st.set_page_config(
    page_title="Russian Stock Market Dashboard",
    page_icon="📈",
    layout="wide"
)

# Initialize API client
@st.cache_resource
def get_client():
    return MOEXClient()

def main():
    # Custom CSS
    st.markdown("""
        <style>
        .stApp {
            max-width: 1200px;
            margin: 0 auto;
        }
        .metric-container {
            background-color: #f0f2f6;
            padding: 1rem;
            border-radius: 0.5rem;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.title("📈 Russian Stock Market Dashboard")
    st.markdown("---")
    
    try:
        client = get_client()
        
        # Fetch top stocks
        with st.spinner("Loading market data..."):
            stocks = client.get_top_stocks()
        
        # Sidebar controls
        selected_ticker = render_stock_selector(stocks)
        time_period = render_time_period_selector()
        
        # Main content
        with st.spinner("Loading stock data..."):
            # Get stock information and candle data
            stock_info = client.get_stock_info(selected_ticker)
            candles = client.get_candles(selected_ticker, time_period)
            
            if not candles.empty:
                # Create and display chart
                fig = create_candlestick_chart(candles, stock_info)
                st.plotly_chart(fig, use_container_width=True)
                
                # Display stock information
                render_stock_info(stock_info)
                
                # Additional stock details
                with st.expander("Detailed Stock Information"):
                    st.json(format_stock_info(stock_info))
            else:
                st.warning("No data available for the selected time period.")
                
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        st.exception(e)

if __name__ == "__main__":
    main()
