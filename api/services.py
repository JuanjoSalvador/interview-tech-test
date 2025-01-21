from abc import ABCMeta, abstractmethod


class APIService(metaclass=ABCMeta):
    class_name = "APIService"

    @abstractmethod
    def all(self, *args, **kwargs):
        pass

    @abstractmethod
    def get(self, *args, **kwargs):
        pass

    @abstractmethod
    def create(self, *args, **kwargs):
        pass

    @abstractmethod
    def update(self, *args, **kwargs):
        pass

    @abstractmethod
    def delete(self, *args, **kwargs):
        pass
  