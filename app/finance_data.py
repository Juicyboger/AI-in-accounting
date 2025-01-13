import yfinance as yf
import logging

logger = logging.getLogger(__name__)

def fetch_sg_stock_price(symbol: str):
    """
    使用yfinance获取新加坡股票的最新收盘价。
    symbol: 类似 'D05.SI' 代表 DBS Bank
    """
    try:
        ticker = yf.Ticker(symbol)
        data = ticker.history(period="1d")  # 获取最近1天的历史数据
        if data.empty:
            logger.warning(f"No data returned from yfinance for {symbol}")
            return None

        latest_price = data["Close"].iloc[-1]
        latest_date = data.index[-1].date()

        return {
            "symbol": symbol,
            "price": f"{latest_price:.2f}",  # 保留2位小数
            "latest_trading_day": str(latest_date)
        }
    except Exception as e:
        logger.error(f"Error fetching yfinance data for {symbol}: {e}")
        return None
