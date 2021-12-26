
from django.urls import path
from auction_app.apps.endpoints.account import accountEndPoint
from auction_app.apps.endpoints.check import checkEndPoint

urlpatterns = [
    path('generate/', accountEndPoint.account_generate, name='generate test account - POST'),
    path('generate/<str:name>&<str:comment>/', accountEndPoint.account_generate, name='generate test account - GET'),
    path('check/', checkEndPoint.account_check, name='check account balance by public key - POST'),
    path('check/<str:publicAddress>/', checkEndPoint.account_check, name='check account balance by public key - GET'),
]