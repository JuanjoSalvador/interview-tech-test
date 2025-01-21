from unittest.mock import MagicMock



def test_get_all_movies_view(
        api_client, 
        mock_firestore_client, 
        mock_firestore_movies
    ):

    mock_db = MagicMock()
    mock_firestore_client.return_value = mock_db
    mock_db.select.return_value.order_by.return_value.offset.return_value.limit.return_value.get.return_value = [
        MagicMock(to_dict=lambda: mock_firestore_movies)
    ]
    response = api_client.get("http://testserver/api/v1/movies/")
    response_json = response.json()

    assert response_json["results"] == [mock_firestore_movies]
    assert response_json.get('total') == 1
    assert response.status_code == 200
    

def test_get_one_movie_view(
        api_client, 
        mock_firestore_client, 
        mock_firestore_movies
    ):

    mock_db = MagicMock()
    mock_firestore_client.return_value = mock_db
    mock_db.document.return_value.get.return_value = MagicMock(to_dict=lambda: mock_firestore_movies)

    movie_id = mock_firestore_movies.get('imdbID', None)
    response = api_client.get(f"http://testserver/api/v1/movies/{movie_id}/")

    # response_json = response.json()

    assert response.status_code == 200
    # assert response_json == mock_firestore_movies
        

def test_get_one_movie_not_exist_view(
        api_client, 
        mock_firestore_client, 
    ):

    mock_db = MagicMock()
    mock_firestore_client.return_value = mock_db
    mock_db.document.return_value.get.return_value = MagicMock(to_dict=lambda: {})

    response = api_client.get("http://testserver/api/v1/movies/non-id-value/")
    
    assert response.status_code == 404
    