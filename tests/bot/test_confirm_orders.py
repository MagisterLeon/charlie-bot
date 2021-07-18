import os


def test_confirm_order_automatically_when_its_in_current_inventory(shroom_market, inventory_api_client, dai,
                                                                   charlie_account, customer_account, utils):
    # given
    offer_id = "psilocybe"
    file_data = utils.build_file_data(offer_id)
    inventory_api_client.post('/inventory', buffered=True, content_type='multipart/form-data', data=file_data)
    dai.approve(shroom_market, 100, {'from': customer_account})

    # when
    shroom_market.ask(b'pkey', charlie_account, bytes(offer_id, encoding='utf-8'), 100, {'from': customer_account})

    # then
    assert not os.path.isfile("./inventory/psilocybe.yaml")
