from rest_framework import generics
from .models import *
from .serializers import *
from .permissions import IsAdminOrReadOnly


class AccountsAPIList(generics.ListCreateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountsSerializers
    permission_classes = (IsAdminOrReadOnly, )

    def get_queryset(self):
        return Account.objects.filter(user=self.request.user)


class OperationsAPIList(generics.ListCreateAPIView):
    queryset = Operation.objects.all()
    serializer_class = OperationsSerializers
    permission_classes = (IsAdminOrReadOnly, )

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        return Operation.objects.filter(account__user=self.request.user).filter(account__pk=pk).order_by('-id')
