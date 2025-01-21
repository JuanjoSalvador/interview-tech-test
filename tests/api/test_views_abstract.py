from api.views.model_view import ModelView


class DummyModelView(ModelView):
    def get(self, *args, **kwargs):
        return super().get(*args, **kwargs)

    def post(self, *args, **kwargs):
        return super().post(*args, **kwargs)

    def put(self, *args, **kwargs):
        return super().put(*args, **kwargs)

    def delete(self, *args, **kwargs):
        return super().delete(*args, **kwargs)


def test_abstract_api_view():
    dummy_model_view = DummyModelView()

    assert dummy_model_view.get() is None
    assert dummy_model_view.post() is None
    assert dummy_model_view.put() is None
    assert dummy_model_view.delete() is None
    assert dummy_model_view.class_name == "ModelView"
