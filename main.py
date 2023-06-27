from config import *
from Modules.Account import Account
from Modules.Minter import mint

def main(secret_key: str):
    nets = SETTINGS.get("UseNets")
    random.shuffle(nets)
    account = Account(secret_key)

    logger.info(f'[{account.address}] Work started')

    for net in nets:
        if mint(account, net):
            logger.info(f'[{account.address}] End work')
            return
        
    logger.error(f'[{account.address}] End work without minted nfts!')
        
    
def runner(task):
    threads = []
    for i in SECRETS:
        threads.append(Thread(
            target=task,
            args=(i,)
        ))
    
    for k in threads:
        k.start()
        time.sleep(get_random_number("ThreadRunnerSleep"))
    
    for j in threads:
        j.join()


if __name__ == "__main__":
    runner(main)