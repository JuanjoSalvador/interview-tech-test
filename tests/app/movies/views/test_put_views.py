import pytest

def test_update_movie(api_client):
    '''
    Test insert new movie into database with invalid data through view.
    '''

    with pytest.raises(NotImplementedError):
        data = {"Type": "movie", "Title": "Mock Movie"}
        response = api_client.put('http://testserver/api/v1/movies/id1/', json=data)   