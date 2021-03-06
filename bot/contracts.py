import json
import sys

from Crypto.PublicKey import RSA
from web3 import Web3
from web3._utils.filters import LogFilter
from web3.types import TxReceipt

from bot.config import settings
from bot.crypto import encrypt
from bot.events import AskEvent
from bot.inventory import Offer
from bot.utils import to_bytes, format_dai_to_decimals


class Contract:

    def __init__(self, address: str, abi_path: str):
        print(f'connecting to {settings.HTTP_PROVIDER_URL}', file=sys.stdout)
        self.w3 = Web3(Web3.HTTPProvider(settings.HTTP_PROVIDER_URL))

        with open(settings.ROOT_DIR + abi_path, 'r') as abi:
            self.contract = self.w3.eth.contract(address=Web3.toChecksumAddress(address), abi=json.load(abi))


class ShroomMarketContract(Contract):

    def __init__(self, address: str, abi_path: str):
        super().__init__(address, abi_path)
        self.seller = settings.USER_ADDRESS

    def get_ask_events_filter(self) -> LogFilter:
        return self.contract.events.Ask.createFilter(fromBlock="latest")

    def did_customer_buy_offer(self, ask: AskEvent, offer_id: bytes) -> bool:
        # TODO can we use hashing function from w3 instead of calling the contract?
        ask_id = self.contract.functions.get_ask_id(self.seller, offer_id, ask.customer_address).call()
        ask_id_total = self.contract.functions.asks(ask_id).call()

        return ask_id_total > 0 and ask_id_total == ask.total

    def confirm_order(self, ask: AskEvent, offer: Offer) -> TxReceipt:
        encrypted_location = encrypt(offer.location, RSA.importKey(ask.customer_public_key))
        tx_hash = self.contract.functions.confirm(ask.customer_address,
                                                  to_bytes(offer.id),
                                                  ask.total,
                                                  encrypted_location
                                                  ).transact({'from': self.seller})

        return self.w3.eth.wait_for_transaction_receipt(tx_hash)


class DaiContract(Contract):

    def get_balance(self) -> str:
        balance = self.contract.functions.balanceOf(settings.USER_ADDRESS).call()
        return format_dai_to_decimals(balance)
