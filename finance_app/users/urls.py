from django.urls import path
from .views import *

app_name = 'users'

urlpatterns = [
    path('registration/', RegistrationUserView.as_view(), name='registration'),
    path('login/', LoginUserView.as_view(), name='login'),
    path('exit/', logout, name='exit'),
]
