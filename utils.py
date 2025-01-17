import plotly.graph_objects as go
import pandas as pd
from typing import Dict

def create_candlestick_chart(candles: pd.DataFrame, stock_info: Dict) -> go.Figure:
    """Create an interactive candlestick chart using Plotly"""
    fig = go.Figure(data=[go.Candlestick(
        x=candles['begin'],
        open=candles['open'],
        high=candles['high'],
        low=candles['low'],
        close=candles['close']
    )])
    
    fig.update_layout(
        title=f"{stock_info.get('SECID', '')} - {stock_info.get('SHORTNAME', '')}",
        yaxis_title='Price (RUB)',
        xaxis_title='Date',
        template='plotly_white',
        height=600,
        xaxis_rangeslider_visible=False
    )
    
    return fig

def format_stock_info(stock_info: Dict) -> Dict:
    """Format stock information for display"""
    return {
        "Ticker": stock_info.get("SECID", "N/A"),
        "Name": stock_info.get("SHORTNAME", "N/A"),
        "ISIN": stock_info.get("ISIN", "N/A"),
        "Lot Size": stock_info.get("LOTSIZE", "N/A"),
        "Face Value": stock_info.get("FACEVALUE", "N/A"),
        "Issue Size": stock_info.get("ISSUESIZE", "N/A"),
        "Currency": stock_info.get("CURRENCYID", "N/A")
    }
