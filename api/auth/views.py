import json

from api.exceptions import FirebaseServiceError

from .interfaces.views import AuthView
from .services import LoginService


class LoginView(AuthView):
    '''
    SECURITY WARNING

    LoginView gets a plain-text password (no encryptation), 
    which is VERY INSECURE for a production environment. This
    view is ONLY INTENDED FOR USING ON LOCAL DEVELOPMENT with
    dummy users.

    For a production environment or using with real users, please
    consider login using Firebase Authentication from frontend.
    '''
    def post(self, req, resp, **kwargs):
        try:
            data = json.loads(req.body)
            email, password = data.get('email', None), data.get('password', None)
            resp.json = LoginService.login(email, password)
        
        except TypeError:
            resp.status_code = 400
            resp.json = {
                "error": 400, 
                "message": "Missing required fields. Make sure 'email' and 'password' are defined."
            }

        except FirebaseServiceError as fse:
            resp.status_code = fse.status

        return resp