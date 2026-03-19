import requests
import time
import telebot
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

TOKEN = "PUT_YOUR_TOKEN_HERE"
CHAT_ID = "PUT_CHAT_ID_HERE"

bot = telebot.TeleBot(TOKEN)

symbol = "GC=F"

def get_signal():
    data = yf.download(symbol, period="1d", interval="5m")
    
    data["MA20"] = data["Close"].rolling(20).mean()
    data["MA50"] = data["Close"].rolling(50).mean()
    
    last = data.iloc[-1]

    if last["MA20"] > last["MA50"]:
        return "BUY", data
    elif last["MA20"] < last["MA50"]:
        return "SELL", data
    else:
        return "WAIT", data


def send_chart(data, signal):
    plt.figure(figsize=(8,4))
    plt.plot(data["Close"], label="Price")
    plt.plot(data["MA20"], label="MA20")
    plt.plot(data["MA50"], label="MA50")
    plt.legend()

    file = "chart.png"
    plt.savefig(file)
    plt.close()

    bot.send_photo(CHAT_ID, open(file,"rb"), caption=f"Signal: {signal}")


while True:
    signal, data = get_signal()

    message = f"""
📊 GOLD SIGNAL

Signal: {signal}
Timeframe: M5
Strategy: Moving Average
"""

    bot.send_message(CHAT_ID, message)

    send_chart(data, signal)

    time.sleep(300)
