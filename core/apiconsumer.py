'''
Created on Oct 30, 2017

@author: javier
'''
from core.async import EventQueue, Message, MessageTicker, MessageOHLCV
from core.dispatcher import Dispatcher
import requests
import logging

class BaseConsumer(EventQueue):
    '''
    classdocs
    '''
    def __init__(self, period, dispatcher):
        '''
        Constructor
        '''
        super().__init__(period)
        self.dispatcher = dispatcher
                    
    def on_message(self, mgs: Message):
        logging.getLogger().debug("BaseConsumer::on_message")

    def on_init(self, msg: Message):
        logging.getLogger().debug("BaseConsumer::on_init")
            
    def on_tick(self, msg: Message):
        logging.getLogger().debug("BaseConsumer::on_tick")
        

    
class TickerConsumer(BaseConsumer):
    def __init__(self, period, dispatcher):
        super().__init__(period, dispatcher)
    
    def on_tick(self, msg: Message):        
        logging.getLogger().debug("TickerConsumer::on_tick")
        #result = self.perform_request("tickerurl")
        #TODO save on db the result and notify the dispatcher
        msg_ticker = MessageTicker()
        msg_ticker.market = "BTC-1ST"
        self.dispatcher.put(msg_ticker)
        
class OHLCVConsumer(BaseConsumer):
    def __init__(self, period, dispatcher):
        super().__init__(period, dispatcher)
    
    def on_tick(self, msg: Message):
        logging.getLogger().debug("OHLCVConsumer::on_tick")    
        #self.perform_request("OHLCVurl")                 
        #TODO save on db the result and notify the dispatcher
        msg_ohlcv = MessageOHLCV()
        msg_ohlcv.market = "BTC-2GIVE"
        self.dispatcher.put(msg_ohlcv)