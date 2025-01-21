
from api.auth.interfaces.views import AuthView

class DummyAuthView(AuthView):
    def post(self, *args, **kwargs):
        return super().post(*args, **kwargs)
    
def test_abstract_api_service():
    dummy_auth_view = DummyAuthView()

    assert dummy_auth_view.post() is None
    assert dummy_auth_view.class_name == "AuthView"
