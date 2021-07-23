import json
import os

from web3 import Web3
from web3.types import TxReceipt

from bot.utils import to_bytes


class Contract:

    def __init__(self, address: str, abi_path: str):
        self.w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))

        with open(os.path.join(os.path.abspath(os.path.dirname(__file__) + "/.."), abi_path), 'r') as abi:
            self.contract = self.w3.eth.contract(address=address, abi=json.load(abi))


class ShroomMarketContract(Contract):

    def confirm_order(self, customer: str, offer: dict, seller: str, total: int) -> TxReceipt:
        offer_id = offer['id']

        tx_hash = self.contract.functions.confirm(customer,
                                                  to_bytes(offer_id),
                                                  total,
                                                  to_bytes(offer['location'])
                                                  ).transact({'from': seller})
        self.w3.eth.wait_for_transaction_receipt(tx_hash)
