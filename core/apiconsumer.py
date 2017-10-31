'''
Created on Oct 30, 2017

@author: javier
'''
from core.async import EventQueue, Message, MessageTicker, MessageOHLCV
from core.dispatcher import Dispatcher
import requests

class BaseConsumer(EventQueue):
    '''
    classdocs
    '''
    def __init__(self, period, dispatcher ,url):
        '''
        Constructor
        '''
        super().__init__(period)
        self.dispatcher = dispatcher
        self.url = url
                    
    def on_message(self, mgs: Message):
        print("BaseConsumer::on_message")

    def on_init(self, msg: Message):
        print("BaseConsumer::on_init")
            
    def on_tick(self, msg: Message):
        print("BaseConsumer::on_tick")
        
    def perform_request(self, url):
        return requests.get(url)
        

    
class TickerConsumer(BaseConsumer):
    def __init__(self, period, dispatcher ,url):
        super().__init__(period, dispatcher, url)
    
    def on_tick(self, msg: Message):        
        print("TickerConsumer::on_tick")
        #result = self.perform_request("tickerurl")
        #TODO save on db the result and notify the dispatcher
        msg_ticker = MessageTicker()
        msg_ticker.markets.append("BTC-1ST")
        self.dispatcher.put(msg_ticker)
        
class OHLCVConsumer(BaseConsumer):
    def __init__(self, period, dispatcher ,url):
        super().__init__(period, dispatcher, url)
    
    def on_tick(self, msg: Message):
        print("OHLCVConsumer::on_tick")    
        #self.perform_request("OHLCVurl")                 
        #TODO save on db the result and notify the dispatcher
        msg_ohlcv = MessageOHLCV()
        msg_ohlcv.markets.append("BTC-2GIVE")
        self.dispatcher.put(msg_ohlcv)

        
        