import pandas as pd
import matplotlib.pyplot as plt
from binance.client import Client

# API Key e Secret
api_key = "WZyninCHpGDplWPzxrRzVkbQcRgZd9U1cCDuJ6DI7caaUx6bjoQ4QrQY802jxJFd"
api_secret = "gUpFgNG60zeDca1SBCJjZEoXDH6nsWkRSOEk2qJDn2tVzXzPpdOBuXr2ExwPDll4"

client = Client(api_key, api_secret)

# Parametri
symbol = "BTCUSDT"
depth_limit = 1000000  # Numero massimo di livelli dell'order book

# Funzione per recuperare l'order book
def fetch_order_book(symbol, limit=100):
    """Recupera l'order book di Binance."""
    order_book = client.get_order_book(symbol=symbol, limit=limit)
    bids = pd.DataFrame(order_book['bids'], columns=['price', 'quantity'], dtype=float)
    asks = pd.DataFrame(order_book['asks'], columns=['price', 'quantity'], dtype=float)
    return bids, asks

# Funzione per identificare zone di liquidità
def identify_liquidity_zones(order_book, threshold_multiplier=2):
    """Identifica le zone di alta liquidità."""
    mean_quantity = order_book['quantity'].mean()
    threshold = mean_quantity * threshold_multiplier
    zones = order_book[order_book['quantity'] > threshold]
    return zones

# Funzione per tracciare il grafico
def plot_order_book(bids, asks, bid_zones, ask_zones, symbol):
    plt.figure(figsize=(14, 8))

    # Plotta i dati dell'order book
    plt.bar(bids['price'], bids['quantity'], color='green', alpha=0.5, label='BID')
    plt.bar(asks['price'], asks['quantity'], color='red', alpha=0.5, label='ASK')
    
    # Evidenzia le zone di liquidità
    plt.scatter(bid_zones['price'], bid_zones['quantity'], color='blue', label='Zone BID Liquide', s=100, zorder=5)
    plt.scatter(ask_zones['price'], ask_zones['quantity'], color='purple', label='Zone ASK Liquide', s=100, zorder=5)
    
    # Aggiungi etichette per le zone di liquidità
    for _, row in bid_zones.iterrows():
        plt.text(row['price'], row['quantity'], f"{row['quantity']:.2f}", color='blue', fontsize=9)
    for _, row in ask_zones.iterrows():
        plt.text(row['price'], row['quantity'], f"{row['quantity']:.2f}", color='purple', fontsize=9)
    
    # Configura il grafico
    plt.xlabel('Prezzo', fontsize=12)
    plt.ylabel('Quantità', fontsize=12)
    plt.title(f"Order Book e Zone di Liquidità per {symbol}", fontsize=16)
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()

    # Mostra il grafico
    plt.show()

# Funzione principale
if __name__ == "__main__":
    print(f"Analizzando l'order book per {symbol}...")
    
    # Recupera l'order book
    bids, asks = fetch_order_book(symbol, limit=depth_limit)
    
    # Identifica le zone di liquidità
    bid_zones = identify_liquidity_zones(bids)
    ask_zones = identify_liquidity_zones(asks)
    current_price= fetch_order_book(symbol, limit=100)
    # Mostra i risultati
    print("\nZone di alta liquidità (BID):")
    print(bid_zones)
    print("\nZone di alta liquidità (ASK):")
    print(ask_zones)
    print (current_price)

    # Visualizza le zone di liquidità
    plot_order_book(bids, asks, bid_zones, ask_zones, symbol)
