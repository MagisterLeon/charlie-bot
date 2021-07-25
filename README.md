#Bot interacting with a marketplace on Ethereum

The goal is to automate operations of fantasy magic shrooms vendor Charlie by writing a bot transacting on
Ethereum.
Charlie delivers goods to customers by revealing secret locations where shrooms are hidden. Since finding
good secret locations and hiding shrooms takes time, Charlie’s inventory in any given moment is limited.
Normally Charlie publishes a list of offers. Customer picks an offer, calls Ethereum smart contract, locking
funds and specifying offer id. Charlie periodically checks Ethereum for new orders. If order sum corresponds
to the offer id and Charlie has the goods, he calls the contract, taking the money and revealing the secret
location to the customer only. Charlie uses etherscan.io and Metamask to interact with Ethereum and finds
it very tedious.
To help Charlie, bot should listen for new orders and confirm them if they are valid and goods are in inventory.
Offer is a yaml file with following fields:

```
- genus: string
- mass: int
- price: int
- id: string
```

Charlie accepts DAI only: https://www.coingecko.com/en/coins/dai
Implementation notes
• Target platform: Linux, but neatly packed into a docker, so usable easily also on MacOS
• Language: python
• Bot should update inventory after each confirmation
• Charlie should be able to inform the bot about new inventory
• Secret locations are text

### Contract
Contract is deployed on mainnet at 0x28c3d91e87d0d5c8b2d9866ec52fe4897f889e5f, it’s ABI and source code
are both here:
https://gist.github.com/paulperegud/c4762ba1741494a4479d8290474a91b8


# Installation

In order to interact with ShroomMarket contract locally you need to have `eth-brownie` installed.
It can be installed from `requirements.txt` file:
```
pip install -r requirements.txt
```

# Local environment

1. Build ganache and bot with
```
$ docker-compose up
```

2. Go to `localhost:5000` in your browser and upload some inventory 

3. Deploy ShroomMarket contract on ganache
```
$ brownie run scripts/deploy_shroom_market_contract.py
```

4. Use `customer_ask` script to act as a customer on ShroomMarket contract.
    Go to a script and change `offer_id` and `offer_price` to values of the inventory you want to
    buy as a customer. Then run  
```
brownie run scripts/customer_ask.py
```
5. Bot is listening on Ask events, confirm them if they are valid 
   and reveal secret location (encrypted with customer public key) in Confirm event.
   
# Mainnet environment

1. Provide correct environment variables into `.env` file in project directory
```
SHROOM_MARKET_CONTRACT_ADDRESS=
USER_ADDRESS=
HTTP_PROVIDER_URL=
```
2. Run bot in docker
```
$ docker-compose up
```

# Run tests
```
brownie test
```
