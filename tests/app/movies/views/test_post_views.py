from unittest.mock import MagicMock


def test_create_movie_view(mock_firestore_collection, api_client):
    """
    Test insert new movie into database with valid data through view.
    """
    mock_query = MagicMock()
    mock_firestore_collection.return_value.document.return_value = mock_query

    data = {
        "imdbID": "mock_id",
        "Type": "movie",
        "Title": "Mock Movie",
        "Year": "2020",
        "Poster": "mock_url",
    }
    response = api_client.post("http://testserver/api/v1/movies/", json=data)
    response_json = response.json()

    assert response.status_code == 200
    assert response_json == data

    mock_firestore_collection.assert_called_once_with("movies")
    mock_firestore_collection.return_value.document.assert_called_once_with("mock_id")
    mock_query.set.assert_called_once_with(data)


def test_create_invalid_movie_view(mock_firestore_collection, api_client):
    """
    Test insert new movie into database with invalid data through view.
    """

    data = {"Type": "movie", "Title": "Mock Movie"}
    response = api_client.post("http://testserver/api/v1/movies/", json=data)

    assert response.status_code == 400
