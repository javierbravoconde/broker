'''
Created on Oct 30, 2017

@author: javier
'''

from queue import Queue
from threading import Thread
import time
import datetime
from core.async import EventQueue, Message
from core.async import MSG_TICKER_PROC, MSG_OHLCV_PROC, MSG_ORDER_PROC
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
        self.order_observers = {}
    
        
    def on_message(self, msg: Message):
        logging.getLogger().debug("Dispatcher::on_message")
        if msg.type == MSG_TICKER_PROC:
            if self.ticker_observers.get(msg.symbol):
                for observer in self.ticker_observers[msg.symbol]:
                    observer.put(msg)

        elif msg.type == MSG_OHLCV_PROC:
            if self.ohlcv_observers.get(msg.symbol):
                for observer in self.ohlcv_observers[msg.symbol]:
                    observer.put(msg)

        elif msg.type == MSG_ORDER_PROC:
            if self.order_observers.get(msg.symbol):
                for observer in self.order_observers[msg.symbol]:
                    observer.put(msg)
             
        

    def on_init(self, msg: Message):
        pass
            
    def on_tick(self, msg: Message):
        pass
    
    def subscribe_to_ticker(self, symbol, strategy):
        logging.getLogger().debug("subscribing to symbol ticker", symbol)
        if self.ticker_observers.get(symbol):
            self.ticker_observers[symbol].append(strategy)
        else:
            self.ticker_observers[symbol] = [strategy]

    def subscribe_to_ohlcv(self, symbol, strategy):
        logging.getLogger().debug("subscribing to symbol history")
        if self.ohlcv_observers.get(symbol):
            self.ohlcv_observers[symbol].append(strategy)
        else:
            self.ohlcv_observers[symbol] = [strategy]

    def subscribe_to_order(self, symbol, observer):
        logging.getLogger().debug("subscribing to symbol order")
        if self.order_observers.get(symbol):
            self.order_observers[symbol].append(observer)
        else:
            self.order_observers[symbol] = [observer]
        