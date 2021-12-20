
from django.urls import path
from auction_app.apps.endpoints.generateAccount import accountEndPoint

urlpatterns = [
    path('generate/', accountEndPoint.account_generate, name='generate test account'),
]