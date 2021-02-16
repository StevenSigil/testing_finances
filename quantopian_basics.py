"""
This wont run - No dependencies installed. Just for notes.
"""

# Zipline
from zipline.api import(symbol,
                        order_target_percent,
                        schedule_function,
                        date_rules,
                        time_rules,
                        )


def initialize(context):
    """
        A function to define things to do at the start of the strategy
    """
    # universe selection
    context.long_portfolio = [
        symbol('AAPL'),
        symbol('CSCO'),
        symbol('AMZN'),
    ]


def handle_data(context, data):

    # Quick way to get the results of your porfolio positions (returns) proved a percentage (0.27, etc) per asset.
    order_target_percent(context.long_portfolio[0], 0.27)
    order_target_percent(context.long_portfolio[1], 0.20)
    order_target_percent(context.long_portfolio[2], 0.53)

    # data.current allows you to do something with each item in your portfolio through the backtest.
    # ie: if CSCO > AAPL: sell CSCO
    long_portfolio_close = data.current(context.long_portfolio, 'close')
    print(long_portfolio_close)

    # Is stale method - Is current data equal to data on date in backtest
    print(data.is_stale(symbol('AAPL')))

    # Can trade method - A check to make sure the individual stock is able to be traded
    # Important to include when working with individual securities.
    if data.can_trade(symbol('AAPL')):
        order_target_percent(symbol('AAPL'), 1.0)

    # PRICE HISTORY --
    # Retrieves the field for the security(s), for each bar_count, on frequency -
    # - ie: bar_count=5, frequency='1d' returns the field for each day for the last 5 days (for each x in dataset).
    price_history = data.history(
        context.long_portfolio, fields='price', bar_count=5, frequency='1d')
    print(price_history)


# ---------------------------------------------------------------------------------------------------------------------------------------- #
# ---------------------------------------------------SCHEDULING CUSTOM FUNCTIONS TO RUN--------------------------------------------------- #
def initialize(context):
    """
        A function to define things to do at the start of the strategy
    """
    # universe selection
    context.long_portfolio = [
        symbol('AAPL'),
        symbol('CSCO'),
        symbol('AMZN'),
    ]

    # Schedule the open and close positions functions at week_start, week_end (minus 30 minuts of mkt close) respecfully
    schedule_function(open_positions, date_rules.week_start(),
                      time_rules.market_open())
    schedule_function(close_positions, date_rules.week_end(),
                      time_rules.market_close(minutes=30))


# Sceduling - Functions that are to be scheduled must have context and data attrs. - Call the funtions in the initialize func.
def open_positions(context, data):
    # Allowcate 30% of portfolio to AAPL
    order_target_percent(context.long_portfolio[0], 0.30)


def close_positions(context, data):
    # Allowcate 0% (remove/close)
    order_target_percent(context.long_portfolio[0], 0)


# ----------------------------------------------------------------------------------------------------------------------------------------------------- #
# --------------------------------------------------- SCHEDULING A REBALANCE AND A CUSTOM RECORDING --------------------------------------------------- #
# NOTE: record() seems to be depricated!

def initialize(context):
    context.amzn = symbol('AMZN')
    context.ibm = symbol('IBM')

    schedule_function(rebalance, date_rules.every_day(), time_rules.market_open())
    schedule_function(record_vars, date_rules.every_day(), time_rules.market_open())

def rebalance(context, data):
    order_target_percent(context.amzn, 0.5)
    order_target_percent(context.ibm, -0.5)

def record_vars(context, data):
    record(amzn_close=data.current(context.amzn, 'close'))
    record(ibm_close=data.current(context.ibm, 'close'))