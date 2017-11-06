'''
Created on Nov 5, 2017

@author: javier
'''

from pymongo import MongoClient
from bson.objectid import ObjectId
import datetime

def saveticker(conn : MongoClient, market, tickerinfo):
        
    db = conn.markets_db
    markets = db.market_collection
        
    tickerinfo["Date"] = datetime.datetime.utcnow()     
    
    if  markets.find_one( { "Market": market }):
        markets.update_one({ "Market": market }, {"$push": {"Tickers": tickerinfo}})
    else:
        market = { "Market" : market, "Tickers" : [tickerinfo] }
        markets.insert_one(market).inserted_id


def getdocument(conn : MongoClient, market):
    db = conn.markets_db
    markets = db.market_collection
    return markets.find_one({"Market": market})

