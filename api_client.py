import requests
from datetime import datetime, timedelta
import pandas as pd
from typing import Dict, Optional, List
import streamlit as st

class MOEXClient:
    BASE_URL = "https://iss.moex.com"
    
    @st.cache_data(ttl=300)  # Cache for 5 minutes
    def get_top_stocks(self) -> pd.DataFrame:
        """Fetch top 30 stocks from MOEX"""
        url = f"{self.BASE_URL}/iss/engines/stock/markets/shares/boards/tqbr/securities.json"
        response = requests.get(url)
        response.raise_for_status()
        
        data = response.json()
        securities = pd.DataFrame(
            data['securities']['data'],
            columns=data['securities']['columns']
        )
        
        # Sort by volume and get top 30
        securities = securities.sort_values('VALTODAY', ascending=False).head(30)
        return securities

    @st.cache_data(ttl=300)
    def get_stock_info(self, ticker: str) -> Dict:
        """Fetch detailed information for a specific stock"""
        url = f"{self.BASE_URL}/iss/engines/stock/markets/shares/boards/tqbr/securities/{ticker}.json"
        response = requests.get(url)
        response.raise_for_status()
        
        data = response.json()
        securities = pd.DataFrame(
            data['securities']['data'],
            columns=data['securities']['columns']
        )
        return securities.iloc[0].to_dict() if not securities.empty else {}

    @st.cache_data(ttl=300)
    def get_candles(self, ticker: str, days: int = 30) -> pd.DataFrame:
        """Fetch candle data for a specific stock"""
        from_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
        till_date = datetime.now().strftime("%Y-%m-%d")
        
        url = f"{self.BASE_URL}/iss/engines/stock/markets/shares/boards/tqbr/securities/{ticker}/candles.json"
        params = {
            "from": from_date,
            "till": till_date,
            "interval": 24  # Daily candles
        }
        
        response = requests.get(url, params=params)
        response.raise_for_status()
        
        data = response.json()
        candles = pd.DataFrame(
            data['candles']['data'],
            columns=data['candles']['columns']
        )
        
        if not candles.empty:
            candles['begin'] = pd.to_datetime(candles['begin'])
        
        return candles
