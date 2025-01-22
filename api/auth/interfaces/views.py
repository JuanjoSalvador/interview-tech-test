from abc import ABC, abstractmethod

"""
Interface for View class
"""


class AuthView(ABC):
    class_name = "AuthView"

    @abstractmethod
    def post(self, *args, **kwargs):
        pass
