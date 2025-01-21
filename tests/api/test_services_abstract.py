from api.services import APIService


class DummyService(APIService):
    def all(self, *args, **kwargs):
        return super().all(*args, **kwargs)

    def get(self, *args, **kwargs):
        return super().get(*args, **kwargs)

    def create(self, *args, **kwargs):
        return super().create(*args, **kwargs)

    def update(self, *args, **kwargs):
        return super().update(*args, **kwargs)

    def delete(self, *args, **kwargs):
        return super().delete(*args, **kwargs)


def test_abstract_api_service():
    dummyService = DummyService()

    assert dummyService.all() is None
    assert dummyService.get() is None
    assert dummyService.create() is None
    assert dummyService.update() is None
    assert dummyService.delete() is None
    assert dummyService.class_name == "APIService"
