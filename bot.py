import time
import pandas as pd
import yfinance as yf

# إعدادات
symbol = "GC=F"  # الذهب
interval = "1m"

def get_data():
    data = yf.download(tickers=symbol, period="1d", interval=interval)
    return data

def calculate_ma(data):
    data["MA20"] = data["Close"].rolling(window=20).mean()
    data["MA50"] = data["Close"].rolling(window=50).mean()
    return data

def check_signal(data):
    last = data.iloc[-1]

    ma20 = data["MA20"].iloc[-1]
    ma50 = data["MA50"].iloc[-1]

    if pd.isna(ma20) or pd.isna(ma50):
        return "WAIT"

    if ma20 > ma50:
        return "BUY"
    elif ma20 < ma50:
        return "SELL"
    else:
        return "HOLD"

def run_bot():
    while True:
        try:
            data = get_data()
            data = calculate_ma(data)
            signal = check_signal(data)

            print(f"Signal: {signal}")

            time.sleep(60)  # كل دقيقة

        except Exception as e:
            print(f"Error: {e}")
            time.sleep(10)

if __name__ == "__main__":
    run_bot()
