from gevent import monkey
monkey.patch_all()
from fastapi import FastAPI
from .control.cmc import Controller as cmcController
import asyncio

app=FastAPI()

@app.get("/BTC-USD")
def btc_usd():
    return cmcController().get_price_BTC()

@app.get("/allcmc")
async def get_all():
    return await cmcController().get_crypto()

@app.get("/ethereum")
def get_ETH():
    return cmcController().get_ETH_info()

@app.get("/random")
async def random_cryptos():
    return await cmcController().random_cryptos()