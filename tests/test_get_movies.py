def test_get_movies(client):
    response = client.get("/api/v1/movies")
    assert response.status_code == 200
    data = response.get_json()
    assert data["success"] is True


def test_filter_by_language(client):

    response = client.get("/api/v1/movies?language=English")

    assert response.status_code == 200


def test_sort_by_rating(client):

    response = client.get("/api/v1/movies?sort_by=rating&order=desc")

    assert response.status_code == 200


def test_filter_by_language_case_insensitive(client):
    response = client.get("/api/v1/movies?language=english")
    assert response.status_code == 200
    data = response.get_json()
    assert data["success"] is True
    movies = data["data"]["movies"]
    assert len(movies) > 0
    for movie in movies:
        assert any(lang.lower() == "english" for lang in movie.get("languages", []))
