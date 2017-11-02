'''
Created on Oct 30, 2017

@author: javier
'''

from core import async
import time
from core.async import Message
from core.async import MSG_STOP
from core.dispatcher import Dispatcher
from core.strategies import StrategyTest
from core.strategies import StrategyTest2
from core.apiconsumer import TickerConsumer, OHLCVConsumer
from exchanges.bittrex.bittrex_feeds import BittrexTicker


if __name__ == '__main__':


    dispatcher = Dispatcher(1)

    tiker_consumer = TickerConsumer(5, dispatcher, "")
    ohlcv_consumer = OHLCVConsumer(5, dispatcher, "")
    bittrex_ticker_consumer = BittrexTicker(5, dispatcher, "")

    test_stg = StrategyTest(10, dispatcher)
    test_stg.subscribe_to_ticker_changes(dispatcher, "BTC-1ST")
    test_stg.subscribe_to_ohlcv_changes(dispatcher, "BTC-2GIVE")

    test_stg = StrategyTest2(10, dispatcher)
    test_stg.subscribe_to_ticker_changes(dispatcher, "BTC-ETH")
    test_stg.subscribe_to_ohlcv_changes(dispatcher, "BTC-LTC")
        
    pass