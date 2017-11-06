from exchanges.bittrex.bittrex import Bittrex
from core.apiconsumer import BaseConsumer
from core.async import Message
from core.async import MessageTicker
from core.async import MessageOHLCV
import pandas as pd
from datetime import datetime

""" 
I would like to be able to update regularly the list of markets and take the new list into account for ticker and OHLVC
What about a simple time for ticker and OHLVC that call a function from BittrexFeed on each tick?
"""

class BittrexTicker(BaseConsumer):

    def __init__(self, period, dispatcher, bittrex_api, markets):
        super().__init__(period, dispatcher)
        self.bittrex_api = bittrex_api
        self.markets = markets

    def on_tick(self, msg: Message):
        print("BittrexTicker::on_tick")

        for market in self.markets:
            output = self.bittrex_api.get_ticker(market)
            if output['success'] == True:
                msg_ticker = MessageTicker()
                msg_ticker.ticker = output['result']
                msg_ticker.symbol = market
                self.dispatcher.put(msg_ticker)


class BittrexOHLCV(BaseConsumer):

    def __init__(self, period, dispatcher, bittrex_api, markets, tick_intervals):
        super().__init__(period, dispatcher)
        self.bittrex_api = bittrex_api
        self.markets = markets
        self.tick_intervals = tick_intervals

    def on_tick(self, msg: Message):
        print("BittrexOHLCV::on_tick")

        for market in self.markets:
            output = self.bittrex_api.get_tick_history(market, self.tick_intervals)
            if output['success'] == True:

                results = output['result']
                for result in results:
                    result['T'] = datetime.strptime(result['T'], "%Y-%m-%dT%H:%M:%S")
                df = pd.DataFrame(output['result'])
                df.set_index('T', inplace=True)

                msg_ohlcv = MessageOHLCV()
                msg_ohlcv.history = df
                msg_ohlcv.symbol = market
                self.dispatcher.put(msg_ohlcv)


class BittrexFeed(BaseConsumer):
    """ Feed from Bittrex

            Attributes:
                bittrex_api (Bittrex):          API for Bittrex queries
                base_currency (string):         Base currency traded
                ticker_period (int):            interval in second for ticker calls
                ohlvc_period (int):             interval in second for ohlvc history calls
                markets:                        list of markets
    """

    def __init__(self, period, dispatcher):
        super().__init__(period, dispatcher)
        self.bittrex_api = Bittrex(None, None)
        self.base_currency = "BTC"
        self.ticker_period = 5
        self.ohlvc_period = 5
        self.ohlvc_interval = 'day'
        self.markets = ["BTC-LTC"] # for testing
        #self._update_markets()

        self.ticker_feed = BittrexTicker(self.ticker_period, self.dispatcher, self.bittrex_api, self.markets)
        self.ohlvc_feed = BittrexOHLCV(self.ticker_period, self.dispatcher, self.bittrex_api, self.markets, self.ohlvc_interval)

    def on_tick(self, msg: Message):
        """ Method called for each period

        This method is used to actualized regularly the list of markets.
        It allows to take into account new markets added to the exchange
        """

        print("BittrexFeed::on_tick")
        self._update_markets()

    def on_init(self, msg: Message):
        print("BittrexFeed::on_init")

    def _update_markets(self):
        """ Update the list of markets available for the base currency

            Update the 'markets' attribute
        """
        self.markets = []
        output = self.bittrex_api.get_markets()
        if output['success'] == True:
            results = output['result']
            for market in results:
                if market['BaseCurrency'] == self.base_currency:
                    self.markets.append(market)
        print(self.markets)
