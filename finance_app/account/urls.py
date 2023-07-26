from django.urls import path
from .views import *

app_name = 'account'

urlpatterns = [
    path('', AllAccountView.as_view(), name='accounts'),
    path('operations/<int:time>/', AllOperationsView.as_view(), name='operations'),
    path('operations/<int:pk>/<int:time>/', OperationsOneAccountView.as_view(), name='operationsOne'),
    path('new/', CreateNewAccountView.as_view(), name='CreateAccount'),
    path('newoperation/', CreateOperationView.as_view(), name='CreateOperation'),
    path('newlimit/', CreateNewLimitView.as_view(), name='CreateLimit'),
    path('limit/', LimitView.as_view(), name='Limit'),
    path('operation/<int:pk>', DeleteOperationView.as_view(), name='DeleteOperation'),
    path('profile/', ProfileView.as_view(), name='profile'),
]
