# app/finance_data.py

import os
import requests

def fetch_sg_stock_price(symbol: str):
    """
    从 Alpha Vantage 获取指定新加坡股票的实时价格。
    symbol: 股票代码（可能需要 Alpha Vantage 支持的格式，如 "D05.SI" 表示DBS银行）
    返回包含最新价格、时间戳等信息的字典
    """
    api_key = os.getenv("ALPHA_VANTAGE_KEY")
    if not api_key:
        raise ValueError("未找到 ALPHA_VANTAGE_KEY，请在环境变量中配置。")

    # Alpha Vantage 的全球实时报价endpoint（Digital & Physical）
    url = "https://www.alphavantage.co/query"
    params = {
        "function": "GLOBAL_QUOTE",
        "symbol": symbol,
        "apikey": api_key
    }
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        # "Global Quote" 示例结构:
        # {
        #   "Global Quote": {
        #       "01. symbol": "IBM",
        #       "05. price": "124.5000",
        #       "07. latest trading day": "2023-08-01",
        #       ...
        #   }
        # }
        
        quote_data = data.get("Global Quote", {})
        if not quote_data:
            return None
        
        result = {
            "symbol": quote_data.get("01. symbol"),
            "price": quote_data.get("05. price"),
            "latest_trading_day": quote_data.get("07. latest trading day")
        }
        return result

    except requests.exceptions.RequestException as e:
        print(f"Error fetching stock price: {e}")
        return None
