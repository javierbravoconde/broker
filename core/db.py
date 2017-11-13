'''
Created on Nov 5, 2017

@author: javier
'''

from pymongo import MongoClient
from bson.objectid import ObjectId
import datetime

MAX_TICKER_NUM = 15

def saveticker(conn : MongoClient, market, tickerinfo):
    
    tickerinfo["Date"] = datetime.datetime.utcnow()
        
    db = conn.markets_db
    markets = db.market_collection
    
    if  market_exits(conn, market) :
        number_tickers = get_number_tickers(conn, market)
        if number_tickers >= MAX_TICKER_NUM : 
            remove_last_ticker(conn, market)
            
        push_ticker_info(conn, market, tickerinfo)
    else:
        create_doc(conn, market, tickerinfo)

def push_ticker_info(conn : MongoClient, market, tickerinfo):
    db = conn.markets_db
    markets = db.market_collection
    markets.update_one({ "Market": market }, {"$push": {"Tickers": tickerinfo}})


def create_doc(conn : MongoClient, market, tickerinfo):
    db = conn.markets_db
    markets = db.market_collection
    market_doc = { "Market" : market, "Tickers" : [tickerinfo] }
    markets.insert_one(market_doc).inserted_id

def market_exits(conn : MongoClient, market):
    db = conn.markets_db
    markets = db.market_collection
    market_docs = list(markets.aggregate( [ { "$match" : { "Market" : market } }, { "$project": { "_id": 0, "Market": 1 } } ] ) )
    return  len(market_docs) > 0

def get_number_tickers(conn : MongoClient, market):
    db = conn.markets_db
    markets = db.market_collection
    res = markets.aggregate( [ { "$match" : { "Market" : market } }, { "$project": { "_id": 0 , "number_tickers": { "$size": "$Tickers" } } } ] )
    
    list_res = list (res)
    
    if res:
        return list_res[0]["number_tickers"]
    else:
        return 0
    

def remove_last_ticker(conn : MongoClient, market):
    db = conn.markets_db
    markets = db.market_collection
    markets.update_one({ "Market": market }, {"$pop": {"Tickers": -1}})


def getdocument(conn : MongoClient, market):
    db = conn.markets_db
    markets = db.market_collection
    return markets.find_one({"Market": market})

