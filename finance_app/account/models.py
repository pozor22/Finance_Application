from django.core.validators import MinValueValidator
from django.db import models, router
from django.contrib.auth.models import User
from django.db.models.deletion import Collector


class Type(models.Model):
    name = models.CharField(max_length=10)

    def __str__(self):
        return f'{self.name}'


class Category(models.Model):
    name = models.CharField(max_length=30)
    # if TypeTransaction == True is a -, if TypeTransaction == False is a +
    TypeTransaction = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.name}'


class Account(models.Model):
    name = models.CharField(max_length=30)
    quantity_money = models.FloatField(default=0)
    target = models.FloatField(default=0)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    type = models.ForeignKey(Type, on_delete=models.PROTECT)

    def __str__(self):
        return f'name: {self.name}; user: {self.user}; type: {self.type}'


class Operation(models.Model):
    price = models.FloatField(validators=[MinValueValidator(0)])
    date = models.DateField()
    notes = models.CharField(max_length=100, null=True, blank=True)
    account = models.ForeignKey(Account, related_name='account', on_delete=models.PROTECT)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)

    def save(self, *args, **kwargs):
        if self.category.TypeTransaction == False:
            account = Account.objects.get(id=self.account.id)
            account.quantity_money = account.quantity_money + self.price
        else:
            account = Account.objects.get(id=self.account.id)
            account.quantity_money = account.quantity_money - self.price
        account.save()
        return super().save(*args, **kwargs)

    def delete(self, using=None, keep_parents=False):
        if self.category.TypeTransaction == False:
            account = Account.objects.get(id=self.account.id)
            account.quantity_money = account.quantity_money - self.price
        else:
            account = Account.objects.get(id=self.account.id)
            account.quantity_money = account.quantity_money + self.price
        account.save()
        if self.pk is None:
            raise ValueError(
                "%s object can't be deleted because its %s attribute is set "
                "to None." % (self._meta.object_name, self._meta.pk.attname)
            )
        using = using or router.db_for_write(self.__class__, instance=self)
        collector = Collector(using=using, origin=self)
        collector.collect([self], keep_parents=keep_parents)
        return collector.delete()

    def __str__(self):
        return f'account: {self.account}; category: {self.category}; price: {self.price}'
