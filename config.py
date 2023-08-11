from web3 import Web3
from time import sleep
import random
import json
from loguru import logger
from threading import Thread
from web3 import HTTPProvider
import asyncio
import web3
from eth_account import Account as acc
import time
import requests


with open("data/secrets.txt") as file:
    SECRETS = [i.replace("\n", "").replace(" ", "") for i in file.readlines()]
    logger.success(f'Was found {len(SECRETS)} addresses')

with open("data/settings.json") as file:
    SETTINGS = json.load(file)


def get_random_number(name: str) -> int:
    return random.randint(SETTINGS[name][0], SETTINGS[name][1])

CONNECTED_RPCS = {}

async def connect_to_all_rpcs():
    for net_name in SETTINGS["RPC"].keys():
        temp = []

        for i in SETTINGS["RPC"][net_name]:
            web3 = Web3(HTTPProvider(i))
            temp.append(web3)
        
        CONNECTED_RPCS.update({net_name: temp})
    logger.success("Soft connected to all custom rpc's")


asyncio.run(connect_to_all_rpcs())

ABI = [
    {
        "inputs": [
            {
                "name": "count", 
                "type": "uint256"
            }
        ],
        "name": "purchase",
        "outputs": [],
        "stateMutability": "payable",
        "type": "function"
    }
]

VALUES = {
    "polygon"   : "matic",
    "bsc"       : "bnb",
    "optimism"  : "eth",
    "avalanche" : "avax",
    "arbitrum"  : "eth",
    "linea"     : "eth" 
}

def req(url: str, **kwargs):
    try:
        resp = requests.get(url, **kwargs)
        if resp.status_code == 200:
            return resp.json()
        else:
            #logger.error("Bad status code, will try again")
            pass
    except Exception as error:
        logger.error(f"Requests error: {error}")

def get_ticker_price(ticker) -> float:
    def __find__(ticker: str, rates: list):
        for k in rates:
            name = k.get("symbol")
            if name == ticker.upper() + 'USDT':
                return float(k.get("price"))
    while True:
        response = req("https://api.binance.com/api/v3/ticker/price")
        if type(response) is list:
            return __find__(ticker, response)
        else:
            print(f'Cant get response from binance, tring again...')
            sleep(5)
