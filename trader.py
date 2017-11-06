'''
Created on Oct 30, 2017

@author: javier
'''

from core import async
import time
from core.async import Message
from core.async import MSG_STOP
from core.dispatcher import Dispatcher
from core.strategies import DummyStrategy
from exchanges.bittrex.bittrex_feeds import BittrexFeed
from core.apiconsumer import TickerConsumer, OHLCVConsumer
from exchanges.bittrex.bittrex_feeds import BittrexTicker
from broker import TestBroker


if __name__ == '__main__':

    dispatcher = Dispatcher(1)
    bittrex_feed = BittrexFeed(60, dispatcher)

    strategy = DummyStrategy(10, dispatcher)
    strategy.subscribe_to_ticker(dispatcher, "BTC-LTC")
    strategy.subscribe_to_ohlcv(dispatcher, "BTC-LTC")

    testBroker = TestBroker(10, dispatcher)
    testBroker.subscribe_to_order(dispatcher, "BTC-LTC")


    pass