import os
import time
import requests
from telegram import Bot
import asyncio

# Mengambil Token & Chat ID dari Environment Variables Render
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

bot = Bot(token=TELEGRAM_TOKEN)

def get_btc_price():
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        return float(data['bitcoin']['usd'])
    except Exception as e:
        print(f"Error fetching price: {e}")
        return None

async def main():
    print("Bot pemantau BTC mulai berjalan di Render...")
    
    current_price = get_btc_price()
    while current_price is None:
        await asyncio.sleep(10)
        current_price = get_btc_price()
        
    last_level = int(current_price // 1000) * 1000
    
    await bot.send_message(
        chat_id=CHAT_ID, 
        text=f"🚀 Bot Aktif di Render!\nHarga BTC saat ini: ${current_price:,.2f}\nPatokan awal: ${last_level:,}"
    )

    while True:
        await asyncio.sleep(60)  # Cek setiap 1 menit
        price = get_btc_price()
        
        if price is None:
            continue
            
        current_level = int(price // 1000) * 1000
        
        if current_level != last_level:
            direction = "🟢 NAIK" if current_level > last_level else "🔴 TURUN"
            change = abs(current_level - last_level)
            
            message = (
                f"{direction} ${change:,}!\n"
                f"Harga BTC: ${price:,.2f}\n"
                f"Level baru: ${current_level:,}"
            )
            
            await bot.send_message(chat_id=CHAT_ID, text=message)
            last_level = current_level

if __name__ == "__main__":
    asyncio.run(main())
