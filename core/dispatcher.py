'''
Created on Oct 30, 2017

@author: javier
'''

from queue import Queue
from threading import Thread
import time
import datetime
from core.async import EventQueue, Message
from core.async import MSG_TICKER_PROC, MSG_OHLCV_PROC
import logging


class Dispatcher(EventQueue):
    '''
    classdocs
    '''

    def __init__(self, period):
        '''
        Constructor
        '''
        super().__init__(period)
        self.ticker_observers = {}
        self.ohlcv_observers = {}
    
        
    def on_message(self, msg: Message):
        logging.getLogger().debug("Dispatcher::on_message")
        if msg.type == MSG_TICKER_PROC:
            for market_modif in msg.markets:
                if self.ticker_observers.get(market_modif):
                    for observer in self.ticker_observers[market_modif]:
                        observer.put(msg)
        elif msg.type == MSG_OHLCV_PROC:
            for market_modif in msg.markets:
                if self.ohlcv_observers.get(market_modif):
                    for observer in self.ohlcv_observers[market_modif]:
                        observer.put(msg)
             
        

    def on_init(self, msg: Message):
        pass
            
    def on_tick(self, msg: Message):
        pass
    
    def subscribe_to_ticker_changes(self, market, strategy):
        logging.getLogger().debug("Dispatcher::subscribe_to_ticker_changes")
        if self.ticker_observers.get(market):
            self.ticker_observers[market].append(strategy)
        else:
            self.ticker_observers[market] = [strategy]

    def subscribe_to_ohlcv_changes(self, market, strategy):
        logging.getLogger().debug("Dispatcher::subscribe_to_ohlcv_changes")
        if self.ohlcv_observers.get(market):
            self.ohlcv_observers[market].append(strategy)
        else:
            self.ohlcv_observers[market] = [strategy]            
        