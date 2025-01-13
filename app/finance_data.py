# app/finance_data.py

import os
import requests
import logging

logger = logging.getLogger(__name__)

def fetch_sg_stock_price(symbol: str):
    """
    从 Alpha Vantage 获取指定新加坡股票的实时价格。
    symbol: 股票代码（可能需要 Alpha Vantage 支持的格式，如 "D05.SI" 表示 DBS 银行）
    返回包含最新价格、时间戳等信息的字典，若获取失败则返回 None
    """
    api_key = os.getenv("ALPHA_VANTAGE_KEY")
    if not api_key:
        raise ValueError("未找到 ALPHA_VANTAGE_KEY，请在环境变量中配置。")

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

        # 日志：打印完整 JSON 或关键字段，方便调试
        logger.info(f"[AlphaVantage] Raw JSON response for {symbol}: {data}")

        # 检查可能的错误字段
        if "Error Message" in data:
            logger.warning(f"Alpha Vantage returned Error Message for symbol={symbol}")
            return None

        if "Note" in data:
            logger.warning(f"Alpha Vantage returned Note (likely API limit reached): {data['Note']}")
            return None
        
        # 正常情况: "Global Quote" 结构
        quote_data = data.get("Global Quote", {})
        if not quote_data or quote_data.get("05. price") in (None, "", "0.0000"):
            logger.warning(f"No valid 'Global Quote' found for {symbol}: {quote_data}")
            return None

        result = {
            "symbol": quote_data.get("01. symbol"),
            "price": quote_data.get("05. price"),
            "latest_trading_day": quote_data.get("07. latest trading day")
        }
        return result

    except requests.exceptions.RequestException as e:
        logger.error(f"[AlphaVantage] RequestException: {e}")
        return None
