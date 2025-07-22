import os
import time
from main import analyze
import telegram

# Ganti ini dengan token bot kamu dari @BotFather
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
# Ganti ini dengan chat_id kamu, bisa grup/individu
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

bot = telegram.Bot(token=TELEGRAM_BOT_TOKEN)

def send_signal(coin, price, rsi, ma):
    message = f"🚨 Signal Ditemukan:\nCoin: {coin}\nHarga: {price}\nRSI: {rsi:.2f}\nMA20: {ma:.2f}"
    bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)

if __name__ == "__main__":
    while True:
        print("🔍 Cek sinyal baru...")
        signals = analyze()
        for coin, price, rsi, ma in signals:
            send_signal(coin, price, rsi, ma)
        time.sleep(3600)  # tiap 1 jam
