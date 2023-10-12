from web3 import Web3

ETH_URL = 'http://127.0.0.1:8545/'
MERCHANT_ADDRESS_EXAMPLE = '0x3c30aB6D9aa4705ae54FE2EA4a046F8aE6E092dD'

w3 = Web3(Web3.HTTPProvider(ETH_URL))


class TransactionRepository:
    def get_last_tx_for_merchant(self, merchant_address: str):
        return {}


def get_merchant_balance(merchant_address: str) -> int:
    return w3.eth.block_number


def get_block_of_last_known_transaction(merchant_address: str) -> dict:
    """ Get the block of the last known ETH transaction from DB"""
    return TransactionRepository().get_last_tx_for_merchant(merchant_address)


def get_last_block() -> int:
    return w3.eth.block_number


def has_txs_in_block_range(from_block_num: int, to_block_num: int = None, exclude_txs: list = None) -> bool:
    if exclude_txs is None:
        exclude_txs = []
    if to_block_num is None:
        to_block_num = w3.eth.block_number

    for block_number in range(from_block_num, to_block_num):
        block_info = w3.eth.get_block(block_number, full_transactions=True)
        txs = [tx for tx in block_info['transactions'] if
               tx['to'] == MERCHANT_ADDRESS_EXAMPLE and tx['hash'] not in exclude_txs]
        if txs:
            return True
    return False


def main():
    merchant_address = MERCHANT_ADDRESS_EXAMPLE

    # 1. Get the last tx from our system
    last_db_tx = get_block_of_last_known_transaction(merchant_address)

    merchant_balance = get_merchant_balance(merchant_address)


    from_block_num = last_db_tx['blockNumber']
    other_txs_exist = has_txs_in_block_range(from_block_num=from_block_num, exclude_txs=[last_db_tx['txid']])
