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
import logging
from logging import config
import os
import json

def setup_logging(
    default_path='logging.json',
    default_level=logging.INFO,
    env_key='LOG_CFG'
):
    """Setup logging configuration
    """
    path = default_path
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = json.load(f)
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)


if __name__ == '__main__':

    setup_logging()    
    logging.getLogger().info("Init app...");


    dispatcher = Dispatcher(1)
    bittrex_feed = BittrexFeed(60, dispatcher)

    strategy = DummyStrategy(10, dispatcher)
    strategy.subscribe_to_ticker(dispatcher, "BTC-LTC")
    strategy.subscribe_to_ohlcv(dispatcher, "BTC-LTC")

    testBroker = TestBroker(10, dispatcher)
    testBroker.subscribe_to_order(dispatcher, "BTC-LTC")


    pass