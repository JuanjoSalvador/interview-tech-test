from unittest.mock import MagicMock


def test_all_pagination(mock_firestore_collection):
    """Prueba la funcionalidad de paginación sin búsqueda."""

    from app.movies.services import MovieService

    # Configurar el mock para devolver documentos simulados
    mock_query = MagicMock()
    mock_firestore_collection.return_value = mock_query
    mock_query.select.return_value.order_by.return_value.offset.return_value.limit.return_value.get.return_value = [
        MagicMock(
            to_dict=lambda: {
                "Type": "movie",
                "Title": "Mock Movie 1",
                "Year": "2020",
                "Poster": "url1",
                "imdbID": "id1",
            }
        ),
        MagicMock(
            to_dict=lambda: {
                "Type": "movie",
                "Title": "Mock Movie 2",
                "Year": "2021",
                "Poster": "url2",
                "imdbID": "id2",
            }
        ),
    ]

    # Llamar a la función con la paginación configurada
    result = MovieService.all(page=1, page_size=2)

    # Verificar el resultado
    assert result["results"] == [
        {
            "Type": "movie",
            "Title": "Mock Movie 1",
            "Year": "2020",
            "Poster": "url1",
            "imdbID": "id1",
        },
        {
            "Type": "movie",
            "Title": "Mock Movie 2",
            "Year": "2021",
            "Poster": "url2",
            "imdbID": "id2",
        },
    ]
    assert result["total"] == 2
    assert result["num_of_pages"] == 1
    assert result["page"] == 1
    assert result["next-page"] == "?page=1&page_size=2"  # Última página
    assert result["last-page"] == "?page=1&page_size=2"


def test_all_with_search(mock_firestore_collection):
    """Prueba la funcionalidad de búsqueda."""

    from app.movies.services import MovieService

    # Configurar el mock para devolver documentos filtrados
    mock_query = MagicMock()
    mock_firestore_collection.return_value = mock_query
    mock_query.select.return_value.where.return_value.order_by.return_value.offset.return_value.limit.return_value.get.return_value = [
        MagicMock(
            to_dict=lambda: {
                "Type": "movie",
                "Title": "Searched Movie",
                "Year": "2022",
                "Poster": "url3",
                "imdbID": "id3",
            }
        ),
    ]

    # Llamar a la función con un término de búsqueda
    result = MovieService.all(page=1, page_size=10, search="searched")

    # Verificar el resultado
    assert result["results"] == [
        {
            "Type": "movie",
            "Title": "Searched Movie",
            "Year": "2022",
            "Poster": "url3",
            "imdbID": "id3",
        },
    ]
    assert result["total"] == 1
    assert result["num_of_pages"] == 1
    assert result["page"] == 1
    assert result["next-page"] == "?page=1&page_size=10"
    assert result["last-page"] == "?page=1&page_size=10"


def test_all_empty_results(mock_firestore_collection):
    """Prueba cuando no hay resultados."""

    from app.movies.services import MovieService

    # Configurar el mock para devolver una lista vacía
    mock_query = MagicMock()
    mock_firestore_collection.return_value = mock_query
    mock_query.select.return_value.order_by.return_value.offset.return_value.limit.return_value.get.return_value = []

    # Llamar a la función sin resultados
    result = MovieService.all(page=1, page_size=10)

    # Verificar el resultado
    assert result["results"] == []
    assert result["total"] == 0
    assert result["num_of_pages"] == 1
    assert result["page"] == 1
    assert result["next-page"] == "?page=1&page_size=10"
    assert result["last-page"] == "?page=1&page_size=10"


def test_all_invalid_page(mock_firestore_collection):
    """Prueba cuando la página es inválida (menor que 1)."""
    # Configurar el mock para devolver documentos simulados

    from app.movies.services import MovieService

    mock_query = MagicMock()
    mock_firestore_collection.return_value = mock_query
    mock_query.select.return_value.order_by.return_value.offset.return_value.limit.return_value.get.return_value = []

    # Llamar a la función con una página inválida
    result = MovieService.all(page=0, page_size=10)

    # Verificar que no haya resultados
    assert result["results"] == []
    assert result["total"] == 0
    assert result["num_of_pages"] == 1
    assert result["page"] == 1
    assert result["next-page"] == "?page=1&page_size=10"
    assert result["last-page"] == "?page=1&page_size=10"
