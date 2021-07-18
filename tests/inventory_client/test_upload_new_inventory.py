import os
from io import BytesIO


def build_file_data(offer_id):
    return {
        'file': (BytesIO(b'file content'), f"{offer_id}.yaml")
    }


def test_upload_one_file(client):
    # given
    file_data = build_file_data("psilocybe")

    # when
    result = client.post('/inventory', buffered=True, content_type='multipart/form-data', data=file_data)

    # then
    assert result.status_code == 200
    assert os.path.isfile("./inventory/psilocybe.yaml")


def test_upload_multiple_files(client):
    # given
    file_data1 = build_file_data("psilocybe")
    file_data2 = build_file_data("agaricus")

    # when
    result1 = client.post('/inventory', buffered=True, content_type='multipart/form-data', data=file_data1)
    result2 = client.post('/inventory', buffered=True, content_type='multipart/form-data', data=file_data2)

    # then
    assert result1.status_code == 200
    assert os.path.isfile("./inventory/psilocybe.yaml")
    assert result2.status_code == 200
    assert os.path.isfile("./inventory/agaricus.yaml")
