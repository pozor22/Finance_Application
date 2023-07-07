from django.shortcuts import render, reverse, HttpResponseRedirect
from django.views import View
from .models import Account, Operation
from .forms import *


class AllAccountView(View):
    def get(self, request, *args, **kwargs):
        user = request.user
        accounts = Account.objects.filter(user=user)
        form = CreateAccountForm()
        context = {
            'accounts': accounts,
            'form': form,
        }
        return render(request, 'account/AllAccount.html', context)

    def post(self, request, *args, **kwargs):
        user = request.user
        form = CreateAccountForm(data=request.POST)
        form.instance.user = user
        form.save()
        return HttpResponseRedirect(reverse('Accounts:accounts'))


class AccountView(View):
    def get(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        form = CreateOperationForm()
        account = Account.objects.get(pk=pk)
        try:
            operations = Operation.objects.filter(account__pk=pk).order_by('-date')
        except:
            operations = None
        context = {
            'account': account,
            'operations': operations,
            'form': form,
        }
        return render(request, 'account/Account.html', context)

    def post(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        form = CreateOperationForm(data=request.POST)
        account = Account.objects.get(pk=pk)
        form.instance.account = account
        form.save()
        return HttpResponseRedirect(reverse('Accounts:account', args=[account.pk]))


class DeleteOperationView(View):
    def get(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        operation = Operation.objects.get(pk=pk)
        operation.delete()
        return HttpResponseRedirect(reverse('Accounts:account', args=[operation.account.pk]))
