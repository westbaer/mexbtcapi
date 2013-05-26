from api import mtgox
from api import bitfinex
from api import bitstamp
import logging

logging.basicConfig()
logging.getLogger(__name__)

apis = [mtgox,
		bitstamp,
		bitfinex,
		]

