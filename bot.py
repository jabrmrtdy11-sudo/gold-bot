import requests
import time

TOKEN = "8478639537:AAG72tL0e_fFyv_RohAJnLmyW91hUNHgQDo"
CHAT_ID = "545193335"

prices = []
last_signal = None


def send(msg):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": msg}
    requests.post(url, data=data)


def get_price():
    try:
        r = requests.get("https://api.gold-api.com/price/XAU")
        return r.json()["price"]
    except:
        return None


def rsi(data):

    gains = []
    losses = []

    for i in range(1, len(data)):
        diff = data[i] - data[i-1]

        if diff > 0:
            gains.append(diff)
        else:
            losses.append(abs(diff))

    avg_gain = sum(gains)/len(gains) if gains else 0.1
    avg_loss = sum(losses)/len(losses) if losses else 0.1

    rs = avg_gain / avg_loss

    return 100 - (100/(1+rs))


while True:

    price = get_price()

    if price:
        prices.append(price)
        print("Gold:", price)

    if len(prices) > 40:
        prices.pop(0)

    if len(prices) < 20:
        time.sleep(8)
        continue

    short_ma = sum(prices[-5:]) / 5
    long_ma = sum(prices[-20:]) / 20

    highest = max(prices[-20:])
    lowest = min(prices[-20:])

    rsi_value = rsi(prices)

    signal = None

    if price > highest and rsi_value < 70:
        signal = "BUY"

    elif price < lowest and rsi_value > 30:
        signal = "SELL"

    elif short_ma > long_ma and rsi_value < 65:
        signal = "BUY"

    elif short_ma < long_ma and rsi_value > 35:
        signal = "SELL"

    if signal != last_signal and signal:

        if signal == "BUY":
            tp1 = price + 7
            tp2 = price + 14
            sl = price - 6
            arrow = "📈"
            trend = "BULLISH"

        else:
            tp1 = price - 7
            tp2 = price - 14
            sl = price + 6
            arrow = "📉"
            trend = "BEARISH"

        msg = f"""
🔥 GOLD VIP SIGNAL 🔥

PAIR: XAUUSD

{arrow} SIGNAL: {signal}

ENTRY: {round(price,2)}

TP1: {round(tp1,2)}
TP2: {round(tp2,2)}

SL: {round(sl,2)}

RSI: {round(rsi_value,2)}

TREND: {trend}

TIMEFRAME: M5
"""

        send(msg)

        print(msg)

        last_signal = signal

    time.sleep(8)
