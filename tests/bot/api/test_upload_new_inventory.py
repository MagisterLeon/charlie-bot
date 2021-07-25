import os

from bot.config import settings


def test_upload_one_inventory(inventory_api_client, utils):
    # given
    file_data = utils.build_file_data("psilocybe", b'content')

    # when
    result = inventory_api_client.post('/inventory', buffered=True, content_type='multipart/form-data', data=file_data)

    # then
    assert result.status_code == 200
    assert os.path.isfile(settings.INVENTORY_PATH + "/psilocybe.yaml")


def test_upload_multiple_inventories(inventory_api_client, utils):
    # given
    file_data1 = utils.build_file_data("psilocybe", b'content')
    file_data2 = utils.build_file_data("agaricus", b'content')

    # when
    result1 = inventory_api_client.post('/inventory', buffered=True, content_type='multipart/form-data',
                                        data=file_data1)
    result2 = inventory_api_client.post('/inventory', buffered=True, content_type='multipart/form-data',
                                        data=file_data2)

    # then
    assert result1.status_code == 200
    assert os.path.isfile(settings.INVENTORY_PATH + "/psilocybe.yaml")
    assert result2.status_code == 200
    assert os.path.isfile(settings.INVENTORY_PATH + "/agaricus.yaml")
