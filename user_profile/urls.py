from django.urls import path
from .views import search, get_stream

urlpatterns=[
    path('', search, name='search'),
    path('get_stream/', get_stream, name='get_stream'),
    #path('get_stream/', proxy_stream, name='get_stream'),
]