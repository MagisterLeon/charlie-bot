
from brownie import ShroomMarket, accounts


def main():
    return ShroomMarket.deploy({'from': accounts[0]})
