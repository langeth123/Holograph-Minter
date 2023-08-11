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

with open('Modules/HolographAbi.json') as f:
    ABI = json.load(f)

