'''
Created on Nov 5, 2017

@author: javier
'''

from pymongo import MongoClient
from bson.objectid import ObjectId

def saveticker(conn : MongoClient, market, tickerinfo):
    #get existing document
    
    db = conn.markets_db
    markets = db.market_collection
    
    if  markets.find_one( { "market": market }):
        markets.update_one({ "market": market }, {"$push": {"tickers": tickerinfo}})
    else:
        market = { "market" : market, "tickers" : [tickerinfo] }
        markets.insert_one(market).inserted_id


    
