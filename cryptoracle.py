import requests
import time
import json
from datetime import datetime


def fetch_price(symbol: str, currency: str = "usd") -> float:
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={symbol}&vs_currencies={currency}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get(symbol, {}).get(currency, 0.0)
    return 0.0


def crypto_sentiment_trend(symbol: str, days: int = 7):
    url = f"https://api.coingecko.com/api/v3/coins/{symbol}/market_chart?vs_currency=usd&days={days}"
    response = requests.get(url)
    if response.status_code != 200:
        return None
    data = response.json()
    prices = data['prices']

    changes = []
    for i in range(1, len(prices)):
        change = (prices[i][1] - prices[i-1][1]) / prices[i-1][1] * 100
        changes.append(change)

    average_change = sum(changes) / len(changes)
    sentiment = "bullish" if average_change > 0 else "bearish"
    return round(average_change, 2), sentiment


def snapshot(symbol: str):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    price = fetch_price(symbol)
    change, sentiment = crypto_sentiment_trend(symbol)

    result = {
        "timestamp": timestamp,
        "symbol": symbol,
        "price_usd": price,
        "7d_avg_change_pct": change,
        "sentiment": sentiment
    }

    filename = f"{symbol}_snapshot_{int(time.time())}.json"
    with open(filename, 'w') as f:
        json.dump(result, f, indent=2)

    print(f"Snapshot saved to {filename}")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Crypto Oracle: Snapshots & Sentiment")
    parser.add_argument("symbol", help="Cryptocurrency symbol (e.g. bitcoin, ethereum)")
    args = parser.parse_args()
    snapshot(args.symbol)
