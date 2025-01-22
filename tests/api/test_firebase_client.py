from google.auth.credentials import AnonymousCredentials


def test_firebase_client(monkeypatch):
    def mock_google_auth_default(scopes=None, request=None):
        return AnonymousCredentials(), "mock-project-id"

    monkeypatch.setattr("google.auth.default", mock_google_auth_default)

    from api.firebase_client import initialize_firebase

    db, firebase_app = initialize_firebase()

    assert db is not None
    assert firebase_app is not None
