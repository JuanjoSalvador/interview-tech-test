from abc import abstractmethod

from .view import View

'''
Interface for View class
'''

class ModelView(View):
    class_name = "ModelView"
    
    @abstractmethod
    def get(self, *args, **kwargs):
        pass

    @abstractmethod
    def post(self, *args, **kwargs):
        pass

    @abstractmethod
    def put(self, *args, **kwargs):
        pass

    @abstractmethod
    def delete(self, *args, **kwargs):
        pass

    