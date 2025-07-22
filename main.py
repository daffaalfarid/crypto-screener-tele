import requests, os, time
import pandas as pd
from datetime import datetime
from ta.momentum import RSIIndicator
from ta.trend import SMAIndicator

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
COINS = ["solana", "pepe", "arb", "cfx", "link", "sui", "hbar", "ton", "bonk", "matic"]

def get_data(coin):
    url = f"https://api.coingecko.com/api/v3/coins/{coin}/market_chart"
    params = {"vs_currency":"usd","days":2,"interval":"hourly"}
    r = requests.get(url, params=params).json()
    df = pd.DataFrame(r["prices"], columns=["time","price"])
    df["volume"] = [v[1] for v in r["total_volumes"]]
    df["time"] = pd.to_datetime(df["time"], unit='ms')
    return df

def analyze(df, coin):
    df["rsi"] = RSIIndicator(df["price"],14).rsi()
    df["ma50"] = SMAIndicator(df["price"],50).sma_indicator()
    df["ma200"] = SMAIndicator(df["price"],200).sma_indicator()
    latest = df.iloc[-1]
    msg = []
    if latest.rsi < 35:
        msg.append(f"RSI oversold ({latest.rsi:.1f})")
    if latest.ma50 > latest.ma200:
        msg.append("MA50 crossed above MA200")
    vol_avg = df.volume.mean()
    if latest.volume > vol_avg * 1.5:
        msg.append(f"Volume spike ▲ {latest.volume/vol_avg:.1f}x")
    if msg:
        price = latest.price
        header = f"🪙 {coin.upper()} @ ${price:.2f}"
        return header + "\n" + "\n".join(msg)
    return None

def run():
    for coin in COINS:
        df = get_data(coin)
        alert = analyze(df, coin)
        if alert:
            requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
                         params={"chat_id":CHAT_ID, "text":alert})

if __name__=="__main__":
    run()
