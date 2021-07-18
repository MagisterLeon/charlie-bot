from io import BytesIO


def test_file_upload(client):
    data = {
        'file': (BytesIO(b'genus: Psilocybe'), 'psilocibe.yaml')
    }

    rv = client.post('/inventory', buffered=True,
                     content_type='multipart/form-data',
                     data=data)
    assert rv.status_code == 200
