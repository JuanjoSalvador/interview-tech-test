import pytest
from unittest.mock import patch

@pytest.fixture
def mock_google_credentials_file(monkeypatch, tmp_path):
    fake_credentials_path = tmp_path / "fake_credentials.json"
    fake_credentials_content = """
    {
        "type": "service_account",
        "project_id": "mock-project-id",
        "private_key_id": "mock-private-key-id",
        "private_key": "-----BEGIN PRIVATE KEY-----\\nMockPrivateKey\\n-----END PRIVATE KEY-----\\n",
        "client_email": "mock-email@mock-project-id.iam.gserviceaccount.com",
        "client_id": "mock-client-id",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/mock-email%40mock-project-id.iam.gserviceaccount.com"
    }
    """
    fake_credentials_path.write_text(fake_credentials_content)

    # Usar monkeypatch para modificar la variable de entorno
    monkeypatch.setenv("GOOGLE_APPLICATION_CREDENTIALS", str(fake_credentials_path))

    yield fake_credentials_path

@pytest.fixture
def api_client():
    from api.api import MoviesAPI

    app = MoviesAPI()

    return app.session()


@pytest.fixture
def mock_firestore_client(mock_google_credentials_file):
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
