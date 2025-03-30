import yfinance as yf

# Define the ticker symbol for Gold Futures (COMEX)
ticker = "GC=F"

# Download historical data (adjust the period as needed)
data = yf.download(ticker, start="2023-01-01", end="2025-01-01")

# Save the data to a CSV file
data.to_csv("gold_futures_data.csv")

print("Data saved as 'gold_futures_data.csv'")
