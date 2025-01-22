import pytest

from unittest.mock import MagicMock

from api.exceptions import DocumentDoesNotExist


def test_get_movie(mock_firestore_collection, mock_firestore_movies):
    '''
    '''

    from app.movies.services import MovieService

    mock_query = MagicMock()
    mock_firestore_collection.return_value = mock_query
    mock_query.document.return_value.get.return_value = MagicMock(
        to_dict=lambda: mock_firestore_movies
    )

    movie_id = mock_firestore_movies.get("imdbID", None)

    # Call the function
    result = MovieService.get(movie_id)

    # Assert the expected result
    assert result is not None
    assert result == mock_firestore_movies


def test_get_movie_not_found(mock_firestore_collection, mock_firestore_movies):
    '''
    '''

    from app.movies.services import MovieService

    mock_query = MagicMock()
    mock_firestore_collection.return_value = mock_query
    mock_query.document.return_value.get.return_value = MagicMock(to_dict=lambda: {})
    movie_id = mock_firestore_movies.get("imdbID", None)

    with pytest.raises(DocumentDoesNotExist):
        result = MovieService.get(movie_id)

        assert result is None
