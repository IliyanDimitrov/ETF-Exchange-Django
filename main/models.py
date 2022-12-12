from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.conf import settings

import uuid

from django.urls import reverse

# Create your models here.

class Address(models.Model):
    house_number = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    postcode = models.CharField(max_length=100)
    country = models.CharField(max_length=100)

    class Meta:
        ordering = ['street', 'city']

    def get_absolute_url(self):
        """Returns the URL to access a particular author instance."""
        return reverse('address-detail', args=[str(self.id)])

    #Returns name of the model  
    def __str__(self):
        """String for representing the Model object."""
        return f'{self.street}, {self.city}'   
    
class ETF(models.Model):
    tag = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    quantity = models.BigIntegerField(validators=[MinValueValidator(0)])
    price = models.DecimalField( max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    
    class Meta:
        ordering = ['name', 'price']

    def get_absolute_url(self):
        """Returns the URL to access a particular author instance."""
        return reverse('etf-detail', args=[str(self.id)])

    #Returns name of the model
    def __str__(self):
        """String for representing the Model object."""
        return f'{self.name}'   
    
class Transaction(models.Model):
    # transaction_id =  models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for this particular transaction across whole database')
    buyer = models.ForeignKey('User_Account', on_delete=models.RESTRICT, null=True)
    etf_id = models.ForeignKey('ETF', on_delete=models.RESTRICT, null=True) #delete
    quantity = models.BigIntegerField(validators=[MinValueValidator(0)])
    unit_cost = models.DecimalField( max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    fee = models.DecimalField( max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    purchase_date = models.DateField(null=True, blank=True)
    
    class Meta:
        ordering = ['buyer', 'purchase_date']

    def get_absolute_url(self):
        """Returns the URL to access a particular author instance."""
        return reverse('transaction-detail', args=[str(self.id)])

    #Returns name of the model
    def __str__(self):
        """String for representing the Model object."""
        return f'{self.etf_id.name} quantity: {self.quantity}' 
    
class User_Account(models.Model):
    user_id = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, null=False, primary_key=True,)
    transaction_id = models.ForeignKey('Transaction', on_delete=models.RESTRICT, null=True) # delete this row
    balance = models.DecimalField( max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    address = models.ForeignKey('Address', on_delete=models.SET_NULL, null=True)
    birth_date = models.DateField(null=True, blank=True)
    phone_number = models.CharField( max_length=20)
    #balance_of_ets
    
    class Meta:
        ordering = ['user_id', 'balance']

    def get_absolute_url(self):
        """Returns the URL to access a particular author instance."""
        return reverse('account-detail', args=[str(self.id)])

    #Returns name of the model
    def __str__(self):
        """String for representing the Model object."""
        # return f'{self.phone_number} {self.balance}' 
        return f'{self.user_id.last_name} {self.user_id.last_name}' 
    