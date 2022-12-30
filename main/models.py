from django.db import models
from django.contrib.auth.models import User


class Order(models.Model):
    ticker = models.CharField(max_length=10)
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    type = models.CharField(max_length=4, choices=[('BUY', 'Buy'), ('SELL', 'Sell')])
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    fulfilled = models.BooleanField(default=False, unique=False)
    fulfilled_date = models.DateTimeField(null=True, blank=True)
    @property
    def total(self):
        return self.price * self.quantity
    def __str__(self):
        return f'{self.ticker} - {self.name} - {self.price} - {self.quantity}'

class Balance(models.Model):
    ticker = models.CharField(max_length=10)
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    @property
    def total(self):
        return self.price * self.quantity
    def __str__(self):
        return f'{self.ticker} - {self.name} - {self.price} - {self.quantity}'