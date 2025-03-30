import backtrader as bt
import pandas as pd
import matplotlib.pyplot as plt

# Define the strategy
class MovingAverageCrossStrategy(bt.Strategy):
    params = (
        ('fast_ma_period', 50),   # Fast moving average period
        ('slow_ma_period', 200),  # Slow moving average period
        ('risk_per_trade', 0.02), # Risk 2% per trade
        ('trailing_stop', 0.03),  # 3% trailing stop loss
    )

    def __init__(self):
        # Initialize moving averages
        self.fast_ma = bt.indicators.SimpleMovingAverage(
            self.data.close, period=self.p.fast_ma_period)
        self.slow_ma = bt.indicators.SimpleMovingAverage(
            self.data.close, period=self.p.slow_ma_period)
        
        # To keep track of pending orders
        self.order = None

        # For trailing stop
        self.trailing_stop_order = None

    def next(self):
        # Check if an order is pending
        if self.order:
            return
            
        # Check if we are in the market
        if not self.position:
            # Buy signal: fast MA crosses above slow MA
            if self.fast_ma[0] > self.slow_ma[0] and self.fast_ma[-1] <= self.slow_ma[-1]:
                self.order = self.buy(size=self.calculate_size())
        else:
            # Sell signal: fast MA crosses below slow MA
            if self.fast_ma[0] < self.slow_ma[0] and self.fast_ma[-1] >= self.slow_ma[-1]:
                self.order = self.sell()
            
            # Implement trailing stop loss if position is open
            if self.position:
                if not self.trailing_stop_order:
                    self.trailing_stop_order = self.sell(
                        exectype=bt.Order.StopTrail, trailpercent=self.p.trailing_stop)

    def calculate_size(self):
        """Calculate the size of the position based on portfolio value and risk per trade."""
        risk_amount = self.broker.getvalue() * self.p.risk_per_trade
        stop_loss_distance = self.data.close[0] * 0.03  # Assuming a 3% stop loss
        size = risk_amount / stop_loss_distance
        return size

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # Order submitted/accepted - no action required
            return
            
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(f'BUY EXECUTED, Price: {order.executed.price:.2f}, Cost: {order.executed.value:.2f}, Comm: {order.executed.comm:.2f}')
            elif order.issell():
                self.log(f'SELL EXECUTED, Price: {order.executed.price:.2f}, Cost: {order.executed.value:.2f}, Comm: {order.executed.comm:.2f}')
                
        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')
            
        # Reset orders
        self.order = None

    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.date(0)
        print(f'{dt.isoformat()}, {txt}')

# Load your data (replace with your commodities futures data)
def load_data():
    # Example: Loading from a CSV file
    # Your CSV should have columns like 'date', 'open', 'high', 'low', 'close', 'volume'
    data = pd.read_csv('gold_futures_data.csv', parse_dates=['date'], index_col='date')
    return bt.feeds.PandasData(dataname=data)

# Set up the backtest
def run_backtest():
    # Initialize Cerebro engine
    cerebro = bt.Cerebro()
    
    # Add strategy
    cerebro.addstrategy(MovingAverageCrossStrategy)
    
    # Load data
    data = load_data()
    cerebro.adddata(data)
    
    # Set initial capital
    cerebro.broker.setcash(100000.0)
    
    # Add commission (0.1% of trade value)
    cerebro.broker.setcommission(commission=0.001)
    
    # Add analyzers
    cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name='sharpe')
    cerebro.addanalyzer(bt.analyzers.DrawDown, _name='drawdown')
    cerebro.addanalyzer(bt.analyzers.Returns, _name='returns')
    
    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
    
    # Run the backtest
    results = cerebro.run()
    
    # Print results
    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
    
    # Print analyzers
    strat = results[0]
    print('Sharpe Ratio:', strat.analyzers.sharpe.get_analysis()['sharperatio'])
    print('Max Drawdown:', strat.analyzers.drawdown.get_analysis()['max']['drawdown'])
    print('Annual Return:', strat.analyzers.returns.get_analysis()['rnorm100'])
    
    # Plot the results
    cerebro.plot(style='candlestick')

if __name__ == '__main__':
    run_backtest()
