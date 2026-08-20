from django.urls import path
from .views import register, login, logout, home


urlpatterns=[
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('', home, name='home'),
]