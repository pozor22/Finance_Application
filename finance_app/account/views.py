from django.db.models import Sum
from django.shortcuts import render, reverse, HttpResponseRedirect
from django.views import View
from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy
from .models import Account, Operation, Category
from .forms import CreateOperationForm, CreateAccountForm
from django.db.models import Count


class AllAccountView(ListView):
    model = Account
    template_name = 'account/AllAccount.html'
    context_object_name = 'accounts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all_money'] = Account.objects.filter(user=self.request.user).aggregate(Sum('quantity_money'))
        context['last_operation'] = Operation.objects.filter(account__user=self.request.user).order_by('-id')[:3]
        top_spending = {}
        for cat in Category.objects.all():
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


class CreateNewAccountView(CreateView):
    form_class = CreateAccountForm
    template_name = 'account/CreateAccount.html'
    success_url = reverse_lazy('Accounts:accounts')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class AccountView(View):
    template_name = 'account/Account.html'

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
        return render(request, self.template_name, context)

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
