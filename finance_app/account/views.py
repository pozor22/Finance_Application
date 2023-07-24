from django.db.models import Sum
from django.http import HttpResponseForbidden
from django.shortcuts import render, reverse, HttpResponseRedirect
from django.views import View
from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy
from .models import Account, Operation, Category, Limit
from .forms import CreateOperationForm, CreateAccountForm
from datetime import datetime
from calendar import monthrange
from braces.views import LoginRequiredMixin


class AllAccountView(LoginRequiredMixin, ListView):
    model = Account
    template_name = 'account/AllAccount.html'
    context_object_name = 'accounts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all_money'] = Account.objects.filter(user=self.request.user).aggregate(Sum('quantity_money'))
        context['last_operation'] = Operation.objects.filter(account__user=self.request.user).order_by('-id')[:3]
        top_spending = {}
        for cat in Category.objects.filter(TypeTransaction=True):
            i = Operation.objects.filter(account__user=self.request.user).filter(category=cat).\
                aggregate(Sum('price'))
            if i['price__sum'] != None:
                top_spending[f'{cat}'] = i['price__sum']
        dict1 = {}
        keyy = ''
        maxx = 0
        for i in range(len(top_spending)):
            for key, value in top_spending.items():
                if value >= maxx:
                    keyy = key
                    maxx = value
                    print(keyy)
            dict1[f'{keyy}'] = maxx
            del top_spending[keyy]
            maxx = 0
            keyy = ''
        context['top_spending'] = dict1
        return context

    def get_queryset(self):
        queryset = super(AllAccountView, self).get_queryset()
        queryset = queryset.filter(user=self.request.user)
        return queryset


# time = 1 all operations, time = 2 operations in this month, time = 3 operations in this month - 1
class AllOperationsView(LoginRequiredMixin, ListView):
    model = Operation
    template_name = 'account/Operations.html'
    context_object_name = 'operations'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all_money'] = Account.objects.filter(user=self.request.user).aggregate(Sum('quantity_money'))
        context['all_account'] = Account.objects.filter(user=self.request.user)
        return context

    def get_queryset(self):
        time = self.kwargs['time']
        queryset = None
        if time == 1:
            queryset = super(AllOperationsView, self).get_queryset()
            queryset = queryset.filter(account__user=self.request.user).order_by('-id')
        elif time == 2:
            today = datetime.today()
            last = monthrange(today.year, today.month)
            first = datetime(today.year, today.month, last[0]).strftime('%Y-%m-%d')
            last = datetime(today.year, today.month, last[1]).strftime('%Y-%m-%d')
            queryset = super(AllOperationsView, self).get_queryset()
            queryset = queryset.filter(account__user=self.request.user).\
                filter(date__range=[first, last]).order_by('-id')
        elif time == 3:
            today = datetime.today()
            last = monthrange(today.year, today.month - 1)
            first = datetime(today.year, today.month - 1, last[0]).strftime('%Y-%m-%d')
            last = datetime(today.year, today.month - 1, last[1]).strftime('%Y-%m-%d')
            queryset = super(AllOperationsView, self).get_queryset()
            queryset = queryset.filter(account__user=self.request.user). \
                filter(date__range=[first, last]).order_by('-id')
        return queryset


class OperationsOneAccountView(LoginRequiredMixin, View):
    template_name = 'account/OperationsOneAccount.html'

    def get(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        time = self.kwargs['time']
        if time == 1:
            context = {
                'all_money': Account.objects.get(pk=pk),
                'operations': Operation.objects.filter(account__user=self.request.user).filter(account__pk=pk)
                .order_by('-id'),
                'accounts': Account.objects.filter(user=self.request.user),
            }
        elif time == 2:
            today = datetime.today()
            last = monthrange(today.year, today.month)
            first = datetime(today.year, today.month, last[0]).strftime('%Y-%m-%d')
            last = datetime(today.year, today.month, last[1]).strftime('%Y-%m-%d')
            context = {
                'all_money': Account.objects.get(pk=pk),
                'operations': Operation.objects.filter(account__user=self.request.user).filter(account__pk=pk)
                .filter(date__range=[first, last]).order_by('-id'),
                'accounts': Account.objects.filter(user=self.request.user),
            }
        elif time == 3:
            today = datetime.today()
            last = monthrange(today.year, today.month - 1)
            first = datetime(today.year, today.month - 1, last[0]).strftime('%Y-%m-%d')
            last = datetime(today.year, today.month - 1, last[1]).strftime('%Y-%m-%d')
            context = {
                'all_money': Account.objects.get(pk=pk),
                'operations': Operation.objects.filter(account__user=self.request.user).filter(account__pk=pk)
                .filter(date__range=[first, last]).order_by('-id'),
                'accounts': Account.objects.filter(user=self.request.user),
            }
        return render(request, self.template_name, context)


class CreateOperationView(LoginRequiredMixin, CreateView):
    form_class = CreateOperationForm
    template_name = 'account/CreateOperation.html'
    success_url = reverse_lazy('Accounts:accounts')

    def get_context_data(self, **kwargs):
        context = super(CreateOperationView, self).get_context_data(**kwargs)
        context['form'].fields['account'].queryset = Account.objects.filter(user=self.request.user)
        return context


class CreateNewAccountView(LoginRequiredMixin, CreateView):
    form_class = CreateAccountForm
    template_name = 'account/CreateAccount.html'
    success_url = reverse_lazy('Accounts:accounts')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class LimitView(LoginRequiredMixin, ListView):
    model = Limit
    template_name = 'account/Limit.html'
    context_object_name = 'limits'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_queryset(self):
        queryset = super(LimitView, self).get_queryset()
        queryset = queryset.filter(user=self.request.user)
        return queryset


class ProfileView(View):
    template_name = 'account/profile.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class DeleteOperationView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        operation = Operation.objects.get(pk=pk)
        operation.delete()
        return HttpResponseRedirect(reverse('Accounts:account', args=[operation.account.pk]))
