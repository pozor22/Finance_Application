from django.db import models
from django.contrib.auth.models import User


class Type(models.Model):
    name = models.CharField(max_length=10)

    def __str__(self):
        return f'id: {self.id}; name: {self.name}'


class Category(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return f'id: {self.id}; name: {self.name}'


class Account(models.Model):
    name = models.CharField(max_length=30)
    quantity_money = models.FloatField(default=0)
    target = models.FloatField(default=0)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    type = models.ForeignKey(Type, on_delete=models.PROTECT)

    def __str__(self):
        return f'name: {self.name}; user: {self.user}; type: {self.type}'


class Operation(models.Model):
    price = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)
    account = models.ForeignKey(Account, on_delete=models.PROTECT)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)

    def __str__(self):
        return f'account: {self.account}; category: {self.category}; price: {self.price}'
