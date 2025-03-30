# Commodity Futures Trading Strategy Backtest

![Backtest Results](https://img.shields.io/badge/Annual_Return-8.96%25-green)
![Risk](https://img.shields.io/badge/Max_Drawdown-5.71%25-yellow)
![Sharpe](https://img.shields.io/badge/Sharpe_Ratio-0.96-blue)

A backtesting system for commodities futures using moving average crossovers, implemented with Backtrader.

## Strategy Overview

**Core Logic:**
- 50-day vs 200-day moving average crossover
- 2% risk per trade position sizing
- 3% trailing stop loss
- 0.1% commission per trade

## Recent Backtest Results (Gold Futures)
| Metric               | Result       |
|----------------------|-------------:|
| Starting Capital     | $100,000.00 |
| Final Value          | $118,639.45 |
| Annual Return        | 8.96%       |
| Max Drawdown         | 5.71%       |
| Sharpe Ratio         | 0.96        |

## Features

- 🚦 Risk-managed position sizing
- 📉 Trailing stop loss protection
- 📊 Performance analytics (Sharpe, Drawdown, Returns)
- 📈 Interactive visualization with candlestick charts

## Requirements

```bash
pip install backtrader pandas matplotlib
```

## Usage
1. **Download your historical price data** in CSV format

2. **Prepare your data** in CSV format with columns `date, open, high, low, close, volume`:

   ```csv
   date,open,high,low,close,volume
   2023-01-01,1800.50,1820.75,1795.25,1810.00,100000
   ```
3. **Replace "gold_futures_data.csv" with your csv filename in backtesting_script.py**
   
4. **Run the backtest**:

   ```bash
   python backtesting_script.py
   ```

5. **Review the results** in the console and the interactive plot.

## Customization

Modify **MovingAverageCrossStrategy** parameters by editing the `params` in the strategy:

```python
params = (
    ('fast_ma_period', 50),    # Change to 20 for faster signals
    ('slow_ma_period', 200),   # Change to 100 for medium-term
    ('risk_per_trade', 0.02),  # Adjust risk to 1-3%
    ('trailing_stop', 0.03)    # Set 2-5% trailing stop
)
```

## Data Sources

- **Yahoo Finance**: Use `GC=F` for gold futures data
- **Quandl**: For commodity futures

## License
MIT License - Free for academic and commercial use
