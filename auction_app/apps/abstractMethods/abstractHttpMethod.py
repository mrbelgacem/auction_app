from abc import ABC, abstractmethod
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from django.http import JsonResponse

@method_decorator(csrf_exempt, name='dispatch')
class AbstractHttpMethod(ABC, View):
    
    @abstractmethod
    def get(self, request) -> JsonResponse:
        '''Receive some information'''
        pass
    
    @abstractmethod
    def post(self, request) -> JsonResponse:
        '''Create a new resource,
        send data to the server'''
        pass
    
    @abstractmethod
    def patch(self, request, itemId) -> JsonResponse:
        '''Partially update, 
        modifies a part of the given resource,
        update a resource if one exists already'''
        pass

    @abstractmethod
    def put(self, request, itemId) -> JsonResponse:
        '''Entirely replaces the given resource,
        if the given resource context does not exist, it will create one'''
        pass
    
    @abstractmethod
    def delete(self, request, itemId) -> JsonResponse:
        '''Remove the given resource'''
        pass