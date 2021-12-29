
from django.urls import path
from auction_app.apps.endpoints.account import accountEndPoint
from auction_app.apps.endpoints.check import checkEndPoint
from auction_app.apps.endpoints.asset import assetEndPoint


urlpatterns = [
    path('generate/', accountEndPoint.account_generate, name='generate test account - POST'),
    path('generate/<str:name>&<str:comment>/', accountEndPoint.account_generate, name='generate test account - GET'),
    path('check/', checkEndPoint.account_check, name='check account balance by public key - POST'),
    path('check/<publicAddress>/', checkEndPoint.account_check, name='check account balance by public key - GET'),
    path('asset/', assetEndPoint.create_asset, name='create asset - POST'),
]