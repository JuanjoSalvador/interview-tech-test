import pytest

from unittest.mock import MagicMock

from api.exceptions import ValidationError


def test_create_movie_object(mock_firestore_collection, mock_validate_post):
    """
    Test insert new movie into database with valid data.
    """

    from app.movies.services import MovieService

    mock_validate_post.return_value = True

    mock_query = MagicMock()
    mock_firestore_collection.return_value.document.return_value = mock_query

    data = {
        "imdbID": "mock_id",
        "Type": "movie",
        "Title": "Mock Movie",
        "Year": "2020",
        "Poster": "mock_url",
    }
    result = MovieService.create(data)

    assert result == data

    mock_validate_post.assert_called_once_with(data)
    mock_firestore_collection.return_value.document.assert_called_once_with("mock_id")
    mock_query.set.assert_called_once_with(data)


def test_create_invalid_movie_object(mock_firestore_collection, mock_validate_post):
    """
    Test insert new movie into database with invalid data.
    """

    from app.movies.services import MovieService

    mock_validate_post.return_value = False

    mock_query = MagicMock()
    mock_firestore_collection.return_value.document.return_value = mock_query

    with pytest.raises(ValidationError):
        data = {}
        result = MovieService.create(data)

        assert result == {}

        mock_validate_post.assert_called_once_with(data)
        not mock_validate_post.assert_called_with(data)
        mock_firestore_collection.return_value.document.assert_called_once_with(
            "mock_id"
        )
        mock_query.set.assert_called_once_with(data)


def test_validate_data_valid():
    from app.movies.services import MovieService

    data = {
        "imdbID": "mock_id",
        "Type": "movie",
        "Title": "Mock Movie",
        "Year": "2020",
        "Poster": "mock_url",
    }
    is_valid = MovieService.validate_post(data)

    assert is_valid is True


def test_validate_data_invalid():
    from app.movies.services import MovieService

    data = {"Title": "Mock Movie", "Year": "2020"}
    is_valid = MovieService.validate_post(data)

    assert is_valid is False
