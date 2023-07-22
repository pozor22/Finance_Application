from django import forms
from .models import Operation, Account


class DateInput(forms.DateInput):
    input_type = 'date'


class CreateOperationForm(forms.ModelForm):
    date = forms.DateField(widget=DateInput)

    class Meta:
        model = Operation
        fields = ('price', 'category', 'notes', 'date', 'account',)


class CreateAccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ('name', 'quantity_money', 'target', 'type')
