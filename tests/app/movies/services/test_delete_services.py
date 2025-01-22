import pytest

from unittest.mock import MagicMock

from api.exceptions import NotAuthorizedException, DocumentDoesNotExist


def test_delete_movie_object_staff(
    mock_firestore_collection,
    mock_firestore_movies,
    mock_get_user_roles,
    mock_validate_token,
):
    """
    Test delete movie from database.
    """

    from app.movies.services import MovieService

    token = "1234"
    movie_id = mock_firestore_movies.get("imdbID", None)

    mock_query = MagicMock()
    mock_firestore_collection.return_value = mock_query
    mock_query.document.return_value.get.return_value.to_dict.return_value = MagicMock(
        to_dict=lambda: mock_firestore_movies
    )

    mock_get_user_roles.return_value = ["staff"]
    mock_validate_token.return_value = None, True

    result = MovieService.delete(movie_id, token)

    assert result is None

    # mock_validate_post.assert_called_once_with(data)
    # mock_firestore_collection.assert_called_once_with("movies")
    # mock_firestore_collection.return_value.document.assert_called_once_with("mock_id")
    # mock_query.set.assert_called_once_with(data)


def test_delete_movie_object_not_staff(
    mock_firestore_collection,
    mock_firestore_movies,
    mock_get_user_roles,
    mock_validate_token,
):
    """
    Test delete movie from database (no permissions)
    """

    from app.movies.services import MovieService

    token = "1234"
    movie_id = mock_firestore_movies.get("imdbID", None)

    mock_query = MagicMock()
    mock_firestore_collection.return_value = mock_query
    mock_query.document.return_value.get.return_value.to_dict.return_value = MagicMock(
        to_dict=lambda: mock_firestore_movies
    )

    mock_get_user_roles.return_value = []
    mock_validate_token.return_value = None, True

    with pytest.raises(NotAuthorizedException):
        result = MovieService.delete(movie_id, token)

        assert result is None


def test_delete_movie_object_document_does_not_exist(
    mock_firestore_collection, mock_get_user_roles, mock_validate_token
):
    """
    Test delete movie from database, where movie does not exist
    """

    from app.movies.services import MovieService

    token = "1234"
    movie_id = None

    mock_query = MagicMock()
    mock_firestore_collection.return_value = mock_query
    mock_query.document.return_value.get.return_value = MagicMock(to_dict=lambda: {})

    mock_get_user_roles.return_value = ["staff"]
    mock_validate_token.return_value = None, True

    with pytest.raises(DocumentDoesNotExist):
        result = MovieService.delete(movie_id, token)

        assert result is None
