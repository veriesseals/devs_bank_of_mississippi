# 3) Make the data models (the “tables”)

# Goal: store users, their accounts (checking + savings), external banks, and transactions.

# banking/models.py

from django.db import models
from django.conf import settings
from django.db import models, transaction

USER = settings.AUTH_USER_MODEL

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(USER, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    
class Account(models.Model):
    CHECKING = "checking"
    SAVINGS = "savings"
    ACCOUNT_TYPES = [(CHECKING, "Checking"), (SAVINGS, "Savings")]
    
    
    user = models.ForeignKey(USER, on_delete = models.CASCADE)
    kind = models.CharField(max_length = 10, choices = ACCOUNT_TYPES)
    balance = models.DecimalField(max_digits = 12, decimal_places = 2, default = 0)
    
    class Meta:
        unique_together = ("user", "kind")
        
    def __str__(self):
        return f"{self.user.username} - {self.kind} (${self.balance})"
    
class ExternalAccount(models.Model):
    user = models.ForeignKey(USER, on_delete = models.CASCADE)
    bank_name = models.CharField(max_length = 120)
    routing_number =  models.CharField(max_length = 9)
    account_number = models.CharField(max_length = 20)
    nickname = models.CharField(max_length = 40, blank = True)
    
    def __str__(self):
        return self.nickname or f"{self.bank_name} ({self.account_number[-4:]})"
    
class Transaction(models.Model):
    DEPOSIT = "deposit"
    WITHDRAW = "withdraw"
    