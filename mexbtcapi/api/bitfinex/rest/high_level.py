# -*- coding: utf-8 -*-

from decimal import Decimal
from functools import partial
from datetime import datetime,timedelta

import mexbtcapi
from mexbtcapi import concepts
from mexbtcapi.concepts.currencies import BTC, USD
from mexbtcapi.concepts.currency import Amount, ExchangeRate
from mexbtcapi.concepts.market import Market as BaseMarket, PassiveParticipant

import urllib
import urllib2
import json

MARKET_NAME= "Bitfinex"
_URL = "https://bitfinex.com/api/v1/"

# Symbols: btcusd, ltcusd, ltcbtc

class BitfinexTicker(concepts.market.Ticker):
	TIME_PERIOD = timedelta(days=1)

class Market(BaseMarket):
	def __init__( self, currency ):
		mexbtcapi.concepts.market.Market.__init__(self, MARKET_NAME, BTC, currency)
		if currency != USD:
			raise Exception("Currency not supported on Bitfinex: " + str(currency))
		self.xchg_factory = partial(ExchangeRate, BTC, USD)

	def json_request(self, url, data=None):
		if data is not None:
			data = urllib.urlencode(data)
			req = urllib2.Request(url, data)
		else:
			req = urllib2.Request(url)
		f = urllib2.urlopen(req)
		jdata = json.load(f)
		return jdata

	def getTicker(self):
		url = _URL + "ticker/btcusd"
		data = self.json_request(url)
		data2 = dict(time=data['timestamp'], average=data['mid'], last=data['last_price'], sell=data['ask'], buy=data['bid'])
		fields= list(BitfinexTicker.RATE_FIELDS)
		fields.remove('low')
		fields.remove('high')

		data3 = dict( [ (x, self.xchg_factory(data2[x])) for x in fields] )
		data3['time']= datetime.utcnow()
		return BitfinexTicker( market=self, **data3 ) 
