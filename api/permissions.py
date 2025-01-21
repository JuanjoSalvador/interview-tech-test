from typing import Tuple

from firebase_admin import auth

from api.firebase_client import db, firebase_app


def _validate_token(token) -> Tuple[str, bool]: # pragma: no cover
    '''
    Check if current user token is valid and not expired
    '''
    try:
        decoded_token = auth.verify_id_token(
            id_token=token, app=firebase_app, check_revoked=True
        )

        email = decoded_token['email']
        is_valid = True
    except (
        auth.ValueError,
        auth.ExpiredIdTokenError, 
        auth.InvalidIdTokenError, 
        auth.RevokedIdTokenError,
        auth.UserDisabledError,
    ):
        email = None
        is_valid = False        
    except auth.CertificateFetchError:
        # print("Error while token verification:", fse)
        email = None
        is_valid = False
    
    return email, is_valid

def _get_user_roles(email) -> list:
    user_roles = (
        db.collection('users').document(email).get().to_dict()
    )

    return user_roles.get('roles', None)


def user_has_roles(token: str, required_roles: list = []) -> bool:
    '''
    Return if user is valid and has required roles for the task
    '''
    email, is_valid = _validate_token(token)
    user_roles = _get_user_roles(email=email)
    has_permission = any(role in required_roles for role in user_roles)
    
    return (is_valid and has_permission)
    