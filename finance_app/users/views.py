from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.models import User
from django.urls import reverse
from django.views import View
from .forms import UserForm, LoginUserForm
from django.contrib import auth


class RegistrationUserView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "users/registration.html", {'form': UserForm()})

    def post(self, request, *args, **kwargs):
        form = UserForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            User.objects.create_user(username=username, password=password)
            return render(request, "users/registration.html", {'form': form})

        return render(request, "users/registration.html", {'form': UserForm()})


class LoginUserView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'users/login.html', {'form': LoginUserForm()})

    def post(self, request, *args, **kwargs):
        form = LoginUserForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user:
                auth.login(request, user)
        else:
            form = LoginUserForm()
        context = {"form": form}
        return render(request, 'users/login.html', context=context)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('Accounts:accounts'))
