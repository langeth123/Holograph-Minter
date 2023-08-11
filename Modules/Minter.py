from config import *
from Modules.Account import *


def mint(account: Account, net_name: str):
    attemps = 0
    while True:
        try:
            mint_address = Web3.to_checksum_address(SETTINGS["ContractAddress"])

            contract, w3 = account.get_contract(mint_address, net_name, token=ABI)
            value = contract.functions.getHolographFeeWei(1).call()
            tx_data = account.get_tx_data(w3, net_name, value=value)
            tx = contract.functions.purchase(1).build_transaction(tx_data)

            hash = account.send_transaction(tx, net_name)
            if account.wait_until_tx_finished(hash, net_name):
                logger.success(f'[{account.address}] Minted nft at net: {net_name}')
                return True
            
        except Exception as error:
            attemps += 1
            if attemps > 5:
                logger.error(f'[{account.address}] More than 5 attemps')
                return
            
            logger.error(f'[{account.address}] Mint error ({net_name}) | {error}')
