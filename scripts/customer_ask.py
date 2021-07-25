from os import path

from brownie import Contract, ShroomMarket, interface, network, config, accounts

from bot.crypto import import_rsa_key_bytes

'''
Change offer_id and offer_price values and send ask transaction to ShroomMarket as a default customer 
'''
offer_id = "offer_1"
offer_price = 100
shroom_market_abi_path = path.abspath(path.dirname(__file__) + "/..") + "/contracts/shroom_market_abi.json"


def main():
    customer = config['networks'][network.show_active()]['customer_address']
    shroom_market_address = config['networks'][network.show_active()]['shroom_market_address']
    shroom_market = Contract.from_abi("ShroomMarket", shroom_market_address, ShroomMarket.abi)

    dai = interface.ERC20(config['networks'][network.show_active()]['dai_address'])
    dai.approve(shroom_market, offer_price, {'from': customer})

    shroom_market.ask(import_rsa_key_bytes("customer_public.pem"), accounts[1], bytes(str(offer_id), 'utf-8'),
                      offer_price, {'from': customer})
