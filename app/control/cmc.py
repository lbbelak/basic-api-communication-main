import grequests
from gevent import monkey as curious_george
curious_george.patch_all(thread=False, select=False)
from requests import Request, Session, exceptions
import json
import backoff
import asyncio
from ..config import Config

headers_cmc = {
    'Accept': 'application/json',
    'X-CMC_PRO_API_KEY': Config.CMC_KEY
}

session = Session()
session.headers.update(headers_cmc)

class Controller():
    
    def __init__(self):
        pass
    
    def get_price_BTC(self):
        response = session.get("https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest" ,params={
                                'slug' : 'bitcoin',
                                'convert': 'USD'
    })
        return response.json()['data']['1']['quote']['USD']['price']
    
    @backoff.on_exception(backoff.expo,
                      (exceptions.RequestException, exceptions.HTTPError),
                      max_time=20)
    async def get_crypto(self):
        response = session.get( "https://pro-api.coinmarketcap.com/v1/cryptocurrency/map")
        response.raise_for_status()
        response= response.json()["data"]
        cryptos = {}
        for crypto in response:
            cryptos[crypto['id']] = (crypto['name'], crypto['symbol'])
            if len(cryptos) > 50:
                break
        return cryptos

    @backoff.on_exception(backoff.expo,
                      (exceptions.RequestException, exceptions.HTTPError),
                      max_time=20)
    async def get_ETH_info(self):
        urls = [ "https://pro-api.coinmarketcap.com/v1/cryptocurrency/info", 
             "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest" 

        ]
        rqs = (grequests.get(url, headers=headers_cmc, params= {"symbol" : "ETH"}) for url in urls)
        requests = grequests.map(rqs)
        [rqs.raise_for_status() for rqs in requests]
        return [resp.json()["data"] for resp in requests]


    backoff.on_exception(backoff.expo,
                      (exceptions.RequestException, exceptions.HTTPError),
                      max_time=20)
    async def random_cryptos(self):
        response = session.get( "https://pro-api.coinmarketcap.com/v1/cryptocurrency/map")
        response.raise_for_status()
        response= response.json()["data"]
        symbols = []
        [symbols.append(crypto["symbol"]) for crypto in response]
        urls = ["https://pro-api.coinmarketcap.com/v1/cryptocurrency/info" for i in range(10)]
        rqs = (grequests.get(url, headers=headers_cmc, params= {"symbol" : symbols[i]}) for i, url in enumerate(urls))
        requests = grequests.map(rqs, size=5)
        [rqs.raise_for_status() for rqs in requests]
        return [resp.json()["data"] for resp in requests]