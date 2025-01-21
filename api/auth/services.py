import json
from datetime import datetime, timedelta

import requests

from app import settings
from api.exceptions import FirebaseServiceError
from api.services import APIService


class LoginService(APIService):
    
    REST_API_URL = "https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword"

    @staticmethod
    def login(email: str, password: str, return_secure_token: bool = True) -> dict:
        payload = json.dumps({
            "email": email,
            "password": password,
            "returnSecureToken": return_secure_token
        })

        r = requests.post(LoginService.REST_API_URL,
                        params={"key": settings.FIREBASE_WEB_API_KEY},
                        data=payload)

        response = r.json()
        expiration_time = int(response['expiresIn'])
        expiration_date = datetime.now() + timedelta(seconds=expiration_time)
        response['expirationDate'] = expiration_date.strftime('%Y-%m-%dT%H:%M:%S.%f')

        if response.get('error'):
            message=response['error']['message']
            status=response['error']['code']

            raise FirebaseServiceError(message, status)
        
        return response