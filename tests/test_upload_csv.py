import io


def test_upload_csv(client):
    csv_content = (
        "title,language,rating,release_date\n"
        "Movie1,English,8.5,2022-01-01\n"
        "Movie2,Hindi,9.0,2023-02-02"
    )

    response = client.post(
        "/api/v1/upload",
        data={
            "file": (io.BytesIO(csv_content.encode("utf-8")), "movies.csv"),
            "content_type": "multipart/form-data",
        },
    )

    assert response.status_code == 200
    data = response.get_json()
    assert data["message"] == "csv uploaded successfully"
    assert data["success"] is True
