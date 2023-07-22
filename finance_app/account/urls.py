from django.urls import path
from .views import *

app_name = 'account'

urlpatterns = [
    path('', AllAccountView.as_view(), name='accounts'),
    path('operations/<int:time>/', AllOperationsView.as_view(), name='operations'),
    path('operations/<int:pk>/<int:time>/', OperationsOneAccountView.as_view(), name='operationsOne'),
    path('new/', CreateNewAccountView.as_view(), name='CreateAccount'),
    path('newoperation/', CreateOperationView.as_view(), name='CreateOperation'),
    path('operation/<int:pk>', DeleteOperationView.as_view(), name='DeleteOperation'),
]
