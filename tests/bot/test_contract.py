from bot.contract import ShroomMarketContract
from bot.utils import to_bytes


def upload_inventory(utils, inventory_api_client, offer_id):
    offer_content = f"""
        genus: Psilocybe
        mass: 10
        price: 100
        id: {offer_id}
        location: 50.654164, 16.512376
        """
    file_data = utils.build_file_data(offer_id, to_bytes(offer_content))
    inventory_api_client.post('/inventory', buffered=True, content_type='multipart/form-data', data=file_data)


def ask_for_offer(dai, shroom_market_contract, customer, seller, offer_id):
    dai.approve(shroom_market_contract, 100, {'from': customer})
    shroom_market_contract.ask(b'pkey', seller, to_bytes(offer_id), 100, {'from': customer})


def test_charlie_should_receive_100_dai_when_confirmed_order(shroom_market, inventory_api_client, dai, charlie_account,
                                                             customer_account, utils):
    # given
    offer_id = "offer_1"
    upload_inventory(utils, inventory_api_client, offer_id)
    ask_for_offer(dai, shroom_market, customer_account, charlie_account, offer_id)

    uut = ShroomMarketContract(shroom_market.address, "contracts/shroom_market_abi.json")
    offer = {"id": offer_id, "location": "location"}

    # when
    uut.confirm_order(customer_account, offer, charlie_account, 100)

    # then
    assert dai.balanceOf(charlie_account) == 100
