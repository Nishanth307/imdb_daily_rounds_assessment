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


def test_upload_csv_various_languages_formats(client):
    csv_content = (
        "title,language,rating,release_date\n"
        "MovieList,\"['english','hindi']\",8.5,2022-01-01\n"
        "MovieSingle,Hindi,9.0,2023-02-02\n"
        "MovieComma,\"Spanish, French\",7.5,2021-05-05"
    )

    response = client.post(
        "/api/v1/upload",
        data={
            "file": (io.BytesIO(csv_content.encode("utf-8")), "movies_var.csv"),
            "content_type": "multipart/form-data",
        },
    )

    assert response.status_code == 200
    data = response.get_json()
    assert data["message"] == "csv uploaded successfully"
    assert data["success"] is True

    # Query the movies and verify languages list for MovieList (2022)
    response = client.get("/api/v1/movies?year=2200") # Wait, MovieList is 2022. Let's query year=2022
    response = client.get("/api/v1/movies?year=2022&limit=100")
    assert response.status_code == 200
    movies_2022 = response.get_json()["data"]["movies"]
    found_list = next((m for m in movies_2022 if m["title"] == "MovieList"), None)
    assert found_list is not None
    assert found_list["languages"] == ["english", "hindi"]

    # Query for MovieSingle (2023)
    response = client.get("/api/v1/movies?year=2023&limit=100")
    assert response.status_code == 200
    movies_2023 = response.get_json()["data"]["movies"]
    found_single = next((m for m in movies_2023 if m["title"] == "MovieSingle"), None)
    assert found_single is not None
    assert found_single["languages"] == ["Hindi"]

    # Query for MovieComma (2021)
    response = client.get("/api/v1/movies?year=2021&limit=100")
    assert response.status_code == 200
    movies_2021 = response.get_json()["data"]["movies"]
    found_comma = next((m for m in movies_2021 if m["title"] == "MovieComma"), None)
    assert found_comma is not None
    assert found_comma["languages"] == ["Spanish", "French"]
