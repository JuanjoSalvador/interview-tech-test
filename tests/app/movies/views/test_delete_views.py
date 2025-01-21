import pytest

from unittest.mock import MagicMock

def test_delete_movie_object_staff(
        mock_firestore_client, 
        mock_firestore_movies, 
        mock_get_user_roles,
        mock_validate_token,
        api_client
    ):
    '''
    Test delete movie from database.
    '''
   
    token = '1234'
    headers = {"Authorization": f"Bearer {token}"}
    movie_id = mock_firestore_movies.get('imdbID', None)

    mock_query = MagicMock()
    mock_firestore_client.return_value = mock_query
    mock_query.document.return_value.get.return_value.to_dict.return_value = MagicMock(
        to_dict=lambda: mock_firestore_movies
    )
    
    mock_get_user_roles.return_value = ['staff']
    mock_validate_token.return_value = None, True    

    response = api_client.delete(
        f'http://testserver/api/v1/movies/{movie_id}/',
        headers=headers
    )

    assert response is not None
    assert response.status_code == 200


def test_delete_movie_object_not_staff(
        mock_firestore_client, 
        mock_firestore_movies, 
        mock_get_user_roles,
        mock_validate_token,
        api_client
    ):
    '''
    Test delete movie from database (no permissions)
    '''
   
    token = '1234'
    headers = {"Authorization": f"Bearer {token}"}
    movie_id = mock_firestore_movies.get('imdbID', None)

    mock_query = MagicMock()
    mock_firestore_client.return_value = mock_query
    mock_query.document.return_value.get.return_value.to_dict.return_value = MagicMock(
        to_dict=lambda: mock_firestore_movies
    )
    
    mock_get_user_roles.return_value = []
    mock_validate_token.return_value = None, True    

    response = api_client.delete(
        f'http://testserver/api/v1/movies/{movie_id}/',
        headers=headers
    )
    
    assert response is not None
    assert response.status_code == 401


def test_delete_movie_object_no_authorization(
        mock_firestore_client, 
        mock_firestore_movies, 
        mock_get_user_roles,
        mock_validate_token,
        api_client
    ):
    '''
    Test delete movie from database (no permissions)
    '''

    movie_id = mock_firestore_movies.get('imdbID', None)

    mock_query = MagicMock()
    mock_firestore_client.return_value = mock_query
    mock_query.document.return_value.get.return_value.to_dict.return_value = MagicMock(
        to_dict=lambda: mock_firestore_movies
    )
    
    mock_get_user_roles.return_value = []
    mock_validate_token.return_value = None, True    

    response = api_client.delete(
        f'http://testserver/api/v1/movies/{movie_id}/',
        headers={}
    )
    
    assert response is not None
    assert response.status_code == 401



def test_delete_movie_object_document_does_not_exist(
        mock_firestore_client, 
        mock_get_user_roles,
        mock_validate_token,
        api_client
    ):
    '''
    Test delete movie from database, where movie does not exist
    '''
   
    token = '1234'
    movie_id = 'movie-id'
    headers = {"Authorization": f"Bearer {token}"}

    mock_query = MagicMock()
    mock_firestore_client.return_value = mock_query
    mock_query.document.return_value.get.return_value = MagicMock(
        to_dict=lambda: {}
    )
    
    mock_get_user_roles.return_value = ['staff']
    mock_validate_token.return_value = None, True    

    response = api_client.delete(
        f'http://testserver/api/v1/movies/{movie_id}/',
        headers=headers
    )
    
    assert response is not None
    assert response.status_code == 400
