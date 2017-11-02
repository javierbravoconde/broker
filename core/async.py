'''
Created on Oct 30, 2017

@author: javier
'''

from queue import Queue
from threading import Thread, Timer


MSG_INIT            = 1
MSG_STOP            = 2
MSG_INTERNAL_TICK   = 3

MSG_TICKER_PROC     = 4
MSG_OHLCV_PROC      = 5


class Message(object):
    '''
    classdocs
    '''

    def __init__(self, msg_type):
        '''
        Constructor
        '''
        self.type = msg_type
        
class MessageTicker(Message):
        def __init__(self):
            super().__init__(MSG_TICKER_PROC)
            self.markets = []
            self.ticker = None

class MessageOHLCV(Message):
        def __init__(self):
            super().__init__(MSG_OHLCV_PROC)
            self.markets = []


class EventQueue(object):
    '''
    classdocs
    '''
    def __init__(self, period):
        '''
        Constructor
        '''
        self.queue = Queue()        
        init_msg = Message(MSG_INIT)
        self.queue.put(init_msg)
        self.running = True
        self.period = period         
        
        if(self.period > 0):
            self.timer = Timer(self.period, self.onTick)
                    
        self.timer.start()
                        
        self.thread = Thread(target=self.process);        
        self.thread.start()
          
    def onTick(self):
        self.timer  = Timer(self.period, self.onTick)
        self.timer.start()
        tick_msg = Message(MSG_INTERNAL_TICK)
        self.put(tick_msg)
            
    
    def put(self, message):
        self.queue.put(message)
        
    def process(self):
        while self.running:
            msg = self.queue.get();
            print("EventQueue msg.type: " + str(msg.type) )
            if msg.type == MSG_INIT:
                print ("base::initializing")
                self.on_init(msg)
            elif msg.type == MSG_STOP:
                print ("base::stopping")
                self.running = False
            elif msg.type == MSG_INTERNAL_TICK:
                print ("base::internal tick")
                self.on_tick(msg)
            else:
                self.on_message(msg)         
                
    def on_message(self, mgs: Message):
        pass

    def on_init(self, msg: Message):
        pass
            
    def on_tick(self, msg: Message):
        pass     
        

