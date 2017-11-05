from exchanges.bittrex.bittrex import Bittrex
from core.apiconsumer import BaseConsumer
from core.async import Message
from core.async import MessageTicker
import logging


class BittrexTicker(BaseConsumer):
    def __init__(self, period, dispatcher, url):
        super().__init__(period, dispatcher, url)
        self._api = Bittrex(None, None)
        self.markets = ['BTC-LTC', 'BTC-NEO', 'BTC-ETH']   # for testing

    def on_tick(self, msg: Message):
        logging.getLogger().debug("BittrexTicker::on_tick")

        for market in self.markets:
            output = self._api.get_ticker(market)
            if output['success'] == True:
                msg_ticker = MessageTicker()
                msg_ticker.ticker = output['result']
                logging.getLogger().info('BittrexTicker %s %s', market, msg_ticker.ticker)
                msg_ticker.markets.append(market)
                self.dispatcher.put(msg_ticker)
            else:
                logging.getLogger().error("error calling Bittrex::get_ticker")