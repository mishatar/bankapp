from django.db import models
from users.models import CustomUser


class Customer(models.Model):
    fname = models.CharField(max_length=255)
    lname = models.CharField(max_length=255)

    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="customer",
    )

    def __str__(self):
        return f'{self.fname} {self.lname}'
    

class Account(models.Model):
    name = models.CharField(max_length=100)

    balance = models.DecimalField(
        default=0,
        max_digits=12,
        decimal_places=2
    )

    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="account",
    )
    def __str__(self):
        return self.name


class Expenses(models.Model):
    """ Расходы. """
    name = models.CharField(max_length=100)
    sum = models.IntegerField(default=0)
    pub_date = models.DateTimeField('Дата добавления', auto_now_add=True)
    account = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        related_name='expenses',
    )

    class Meta:
        ordering = ["-pub_date"]

    def __str__(self):
        return self.name


class Income(models.Model):
    """ Доходы. """
    name = models.CharField(max_length=100)
    sum = models.IntegerField(default=0)
    pub_date = models.DateTimeField('Дата добавления', auto_now_add=True)
    account = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        related_name='income',
    )

    class Meta:
        ordering = ["-pub_date"]

    def __str__(self):
        return self.name


class Goals(models.Model):
    """ Цели. """
    name = models.CharField(max_length=100)
    sum_goal = models.IntegerField()
    pub_date = models.DateTimeField('Дата добавления', auto_now_add=True)
    date_goal = models.DateField('Дата желаемого выполнения цели')
    account = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        related_name='goals',
    )

    class Meta:
        ordering = ["-pub_date"]

    def __str__(self):
        return self.name


class Wallet(models.Model):
    balance = models.IntegerField()


class Transfer(models.Model):

    from_account = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        related_name='from_account'
    )

    to_account = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        related_name='to_account'
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )