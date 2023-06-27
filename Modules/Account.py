
from config import (
    CONNECTED_RPCS,
    acc,
    logger,
    random,
    web3,
    SETTINGS,
    Web3,
    time,
    json,
    sleep,
    get_random_number
)

def get_w3(net_name: str):
    w3 = random.choice(CONNECTED_RPCS.get(net_name))
    return w3

class Account:
    def __init__(self, secret_key: str) -> None:
        self.eth_account = acc.from_key(secret_key)
        self.address = self.eth_account.address
        self.secret_key = secret_key

    def wait_until_tx_finished(self, hash: str, net_name: str, max_wait_time=180) -> bool:
        start_time = time.time()
        w3 = get_w3(net_name)
        while True:
            try:
                receipts = w3.eth.get_transaction_receipt(hash)
                status = receipts.get("status")

                if status == 1:
                    logger.success(f"{hash} is completed")
                    return True
                elif status is None:
                    #print(f'[{hash}] still processed')
                    sleep(0.3)
                elif status != 1:
                    logger.error(f'[{self.address}] [{hash}] transaction is failed')
                    return False
            except web3.exceptions.TransactionNotFound:
                #print(f"[{hash}] still in progress")
                if time.time() - start_time > max_wait_time:
                    logger.error(f'FAILED TX: {hash}')
                    return False
                sleep(1)

    def get_contract(self, token_address: str, net_name: str, token):
        w3 = get_w3(net_name)

        contract = w3.eth.contract(token_address, abi=token)
        return contract, w3
    
    def send_transaction(self, tx: dict, net_name: str) -> str: 
        w3 = get_w3(net_name)

        gasEstimate = w3.eth.estimate_gas(tx)
        tx['gas'] = round(gasEstimate * 1.05)
        signed_txn = w3.eth.account.sign_transaction(tx, private_key=self.eth_account.key)

        tx_token = w3.to_hex(w3.eth.send_raw_transaction(signed_txn.rawTransaction))
        logger.success(f"Approved: {tx_token}")

        return tx_token
    
    def get_gas_price(self, net_name: str, gas_price_=False):
        global SETTINGS
        if gas_price_ is not False:
            return Web3.to_wei(gas_price_, 'gwei')
        while True:
            try:
                
                w3 = get_w3(net_name)
                max_gas = Web3.to_wei(SETTINGS.get("GWEI").get(net_name), 'gwei')
                if net_name == 'bsc' and max_gas == Web3.to_wei(1, 'gwei'):
                    return Web3.to_wei(1, 'gwei')

                gas_price = w3.eth.gas_price * 1.05
                if gas_price > max_gas:
                    h_gas, h_max = Web3.from_wei(gas_price, 'gwei'), Web3.from_wei(max_gas, 'gwei')
                    logger.error(f'[{self.address}] Sender net: {net_name}. Current gasPrice: {h_gas} | Max gas price: {h_max}')
                    sleeping(f'[{self.address}] Waiting best gwei. Update after ')

                else:
                    return round(gas_price)
                
            except Exception as error:
                logger.error(f'[{self.address}] Error: {error}')
                sleeping(f'[{self.address}] Error fault. Update after ')

    def get_tx_data(self, w3: Web3, net_name: str, value=0, gas_price_=False) -> dict:
        gas_price = self.get_gas_price(net_name, gas_price_=gas_price_)
        data = {
            'chainId': w3.eth.chain_id, 
            'nonce': w3.eth.get_transaction_count(self.address),  
            'from': self.address, 
            "value": value
        }
        if net_name in ["avalanche", "polygon", "arbitrum", "ethereum"]:
            data["type"] = "0x2"

        if net_name not in ['arbitrum', "avalanche", "polygon", "ethereum"]:
            data["gasPrice"] = gas_price
            
        else:
            data["maxFeePerGas"] = gas_price
            if net_name == "polygon":
                data["maxPriorityFeePerGas"] = Web3.to_wei(30, "gwei")
            elif net_name == "avalanche":
                data["maxPriorityFeePerGas"] = gas_price
            elif net_name == "ethereum":
                data["maxPriorityFeePerGas"] = Web3.to_wei(0.05, "gwei")
            elif net_name == "arbitrum":
                data["maxPriorityFeePerGas"] = Web3.to_wei(0.01, "gwei")
        return data
    
    def get_balance(self, token_address=None, net_name=None, contract=False):
        while True:
            try:
                if contract == False:
                    contract, w3 = self.get_contract(token_address, net_name)
                decimals    = contract.functions.decimals().call()
                balance     = contract.functions.balanceOf(self.address).call()

                from_wei_balance = balance / 10**decimals

                return balance, from_wei_balance
            except Exception as error:
                logger.error(f'[{self.address}] Cant get balance of: {token_address}! Error: {error}')
                self.sleeping()

    def get_native_balance(self, net_name: str):
        while True:
            try:
                w3 = get_w3(net_name)
                balance = w3.eth.get_balance(self.address)

                return balance
            except Exception as error:
                logger.error(f'[{self.address}] Cant get balance of native: {net_name}! Error: {error}')
                self.sleeping()


    def approve_token(self, token_address: str, net_name: str, spender: str):
        def __check_allowance__():
            amount_approved = contract.functions.allowance(self.address, spender).call()

            if amount_approved < balance:
                while True:
                    try:
                        tx = contract.functions.approve(spender, balance).build_transaction(
                            self.get_tx_data(w3, net_name)
                        )
                        return tx
                    except Exception as error:
                        logger.error(f'[{self.address}] Got error while trying approve token: {error}')
                        sleeping(f'[{self.address}] Error fault. Update after ')

        contract, w3 = self.get_contract(token_address, net_name)
        while True:
            balance, human_balance = self.get_balance(contract=contract)
            check_data = __check_allowance__()
            if check_data:
                try:
                    tx_hash = self.send_transaction(check_data, net_name)
                    if self.wait_until_tx_finished(tx_hash, net_name):
                        sleeping("")
                        return
                    else:
                        sleeping(f'[{self.address}] Tx is failed. Will retry approve token ')
                except Exception as error:
                    logger.error(f'[{self.address}] Cant submit tx! Error: {error}')
                    sleeping(f'[{self.address}] Error fault. Update after ')
            else:
                return
            
    def sleeping(self):
        sleeping(f'[{self.address}] | sleeping') # да, костыль, делал на скорую руку


def sleeping(text: str):
    logger.info(text)
    sleep(get_random_number("ErrorSleepTiming"))