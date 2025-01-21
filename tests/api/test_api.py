import pytest

def test_api_method_not_allowed(api_client):
    with pytest.raises(AttributeError):
        response = api_client.options('http://testserver/api/v1/movies/')

        assert response is not None

def test_api_missing_route(api_client):
    response = api_client.post('http://testserver/missing-view/')

    assert response is not None
    assert response.status_code == 404