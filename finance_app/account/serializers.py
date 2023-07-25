from rest_framework import serializers

from .models import *


class AccountsSerializers(serializers.ModelSerializer):
    user = serializers.CharField()

    class Meta:
        model = Account
        fields = "__all__"


class OperationsSerializers(serializers.ModelSerializer):
    category = serializers.CharField()

    class Meta:
        model = Operation
        fields = "__all__"
