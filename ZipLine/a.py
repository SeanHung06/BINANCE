from zipline.api import order, record, symbol, set_benchmark, order_target
import zipline
import matplotlib.pyplot as plt
from datetime import datetime
from zipline.finance import commission
import numpy as np

result = []
for strategy_params in range(1, 3, 1):


def initialize(context):
    context.time = 0
    context.asset = symbol('SPY')
    context.set_commission(commission.PerShare(cost=0.001, min_trade_cost=0))
    context.strategy_params_1 = ta_params
    set_benchmark(symbol("SPY"))


def handle_data(context, data):


context.time += 1
if context.time < 200:
return

# Compute averages
# data.history() has to be called with the same params
# from above and returns a pandas dataframe.
hist = data.history(context.asset, ['close', 'high'], 50, '1d')
if(context.strategy_params == 1):
short_mavg = ta.SMA(hist['close'].values, 5)
long_mavg = ta.SMA(hist['close'].values, 20)
conidition_1 = short_mavg[-1] > long_mavg[-1]
conidition_2 = short_mavg[-1] < long_mavg[-1]
elif (context.strategy_params == 2):
short_mavg = ta.EMA(hist['close'].values, 5)
long_mavg = ta.EMA(hist['close'].values, 20)
conidition_1 = short_mavg[-1] > long_mavg[-1]
conidition_2 = short_mavg[-1] < long_mavg[-1]

record(SPY=data.current(symbol('SPY'), 'price'))

# Trading logic
if conidition_1:
    # order_target orders as many shares as needed to
    # achieve the desired number of shares.
order_target(context.asset, 100)
elif conidition_2:
order_target(context.asset, 0)

# Save values for later inspection
record(price=data.current(context.asset, 'price'),
       moving_average=long_mavg
       )


def analyze(context, perf):


fig, ax = plt.subplots(3, 1, sharex=True, figsize=[16, 9])

# portfolio value
perf.portfolio_value.plot(ax=ax[0])
ax[0].set_ylabel('portfolio value in $')

# asset
perf[['price', 'moving_average']].plot(ax=ax[1])
ax[1].set_ylabel('price in $')

# mark transactions
perf_trans = perf.loc[[t != [] for t in perf.transactions]]
buys = perf_trans.loc[[t[0]['amount'] > 0 for t in perf_trans.transactions]]
sells = perf_trans.loc[[t[0]['amount'] < 0 for t in perf_trans.transactions]]
ax[1].plot(buys.index, perf.price.loc[buys.index],
           '^', markersize=10, color='g', label='buy')
ax[1].plot(sells.index, perf.price.loc[sells.index],
           'v', markersize=10, color='r', label='sell')
ax[1].legend()

# daily returns
perf.returns.plot(ax=ax[2])
ax[2].set_ylabel('daily returns')

fig.suptitle('Simple Moving Average Strategy - Apple', fontsize=16)
plt.legend()
plt.show()

print('Final portfolio value (including cash): {}$'.format(
    np.round(perf.portfolio_value[-1], 2)))

perf = zipline.run_algorithm(start=datetime(2000, 1, 5, 0, 0, 0, 0, pytz.utc),
                             end=datetime(2018, 3, 1, 0, 0, 0, 0, pytz.utc),
                             initialize=initialize,
                             capital_base=100,
                             handle_data=handle_data,
                             analyze=analyze,
                             data=panel)
result.append(perf.portfolio_value[-1])
