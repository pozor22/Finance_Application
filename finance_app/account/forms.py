from django import forms
from .models import Operation, Account


class CreateOperationForm(forms.ModelForm):
    class Meta:
        model = Operation
        fields = ('price', 'category',)


class CreateAccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ('name', 'quantity_money', 'target', 'type')
