import io


def test_invalid_file_type(client):

    response = client.post(
        "/api/v1/upload",
        data={"file": (io.BytesIO(b"hello"), "test.txt")},
        content_type="multipart/form-data",
    )

    assert response.status_code == 400
