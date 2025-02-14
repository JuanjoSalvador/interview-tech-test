from unittest.mock import MagicMock


def test_get_user_roles_with_staff(
    mock_firestore_collection,
):
    from api.auth.permissions import _get_user_roles

    email = "test@example.org"

    mock_query = MagicMock()
    mock_firestore_collection.return_value = mock_query
    mock_query.document.return_value.get.return_value = MagicMock(
        to_dict=lambda: {"roles": ["staff"]}
    )

    user_roles = _get_user_roles(email=email)

    assert user_roles is not None
    assert "staff" in user_roles


def test_get_user_roles_without_role(mock_firestore_collection):
    from api.auth.permissions import _get_user_roles

    email = "test@example.org"

    mock_query = MagicMock()
    mock_firestore_collection.return_value = mock_query
    mock_query.document.return_value.get.return_value = MagicMock(
        to_dict=lambda: {"roles": []}
    )

    user_roles = _get_user_roles(email=email)

    assert user_roles is not None
    assert user_roles == []
