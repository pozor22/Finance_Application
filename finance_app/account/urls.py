from django.urls import path
from .views import *

app_name = 'account'

urlpatterns = [
    path('', AllAccountView.as_view(), name='accounts'),
    path('account/<int:pk>', AccountView.as_view(), name='account'),
    path('operation/<int:pk>', DeleteOperationView.as_view(), name='DeleteOperation'),
]
