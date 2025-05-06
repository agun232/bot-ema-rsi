import requests
import time

TOKEN = 'ISI_TOKEN_BOT'
CHAT_ID = 'ISI_CHAT_ID'
PAIR = 'EURUSD'
TIMEFRAME = '15'  # Menit
EMA_PERIOD = 50
RSI_PERIOD = 14

def get_price():
    url = f"https://api.forexrateapi.com/v1/latest?pair={PAIR}&apikey=demo"
    response = requests.get(url)
    return float(response.json()['rate'])

def get_rsi_and_ema(prices):
    import talib
    import numpy as np
    np_prices = np.array(prices)
    ema = talib.EMA(np_prices, timeperiod=EMA_PERIOD)
    rsi = talib.RSI(np_prices, timeperiod=RSI_PERIOD)
    return ema[-1], rsi[-1]

def send_signal(msg):
    url = f"https://api.telegram.org/bot{7968068833:AAErR3bUAGr2i4EY1IEdZu_nw3cmt97JReE}/sendMessage"
    data = {'chat_id': 1475169664, 'text': msg}
    requests.post(url, data=data)

# Simulasi harga (karena tidak ada MT5)
prices = []

while True:
    price = get_price()
    prices.append(price)
    if len(prices) > EMA_PERIOD:
        ema, rsi = get_rsi_and_ema(prices[-EMA_PERIOD-1:])
        if price > ema and rsi < 30:
            send_signal(f"BUY {PAIR}\nPrice: {price:.2f}, EMA: {ema:.2f}, RSI: {rsi:.2f}")
        elif price < ema and rsi > 70:
            send_signal(f"SELL {PAIR}\nPrice: {price:.2f}, EMA: {ema:.2f}, RSI: {rsi:.2f}")
    time.sleep(900)  # 15 menit
