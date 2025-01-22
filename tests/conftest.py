import pytest
from unittest.mock import patch


@pytest.fixture
def app(monkeypatch):
    monkeypatch.setenv("GOOGLE_APPLICATION_CREDENTIALS", "tests/fake-credentials.json")

    from api.api import MoviesAPI

    return MoviesAPI()


@pytest.fixture
def api_client(app):
    return app.session()


@pytest.fixture
def mock_firestore_client():
    with patch("api.firebase_client.db.collection") as mock_collection:
        yield mock_collection


@pytest.fixture
def mock_firestore_movies():
    return {
        "Type": "movie",
        "Title": "Mock Movie 1",
        "Year": "2020",
        "Poster": "url1",
        "imdbID": "id1",
    }


@pytest.fixture
def mock_validate_post():
    with patch("app.movies.services.MovieService.validate_post") as validate_post:
        yield validate_post


@pytest.fixture
def mock_validate_user():
    with patch("api.permissions.user_has_roles") as validate_user:
        yield validate_user


@pytest.fixture
def mock_get_user_roles():
    with patch("api.permissions._get_user_roles") as get_user_roles:
        yield get_user_roles


@pytest.fixture
def mock_validate_token():
    with patch("api.permissions._validate_token") as validate_token:
        yield validate_token
