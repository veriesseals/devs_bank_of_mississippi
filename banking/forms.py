# forms.py
# ----------------------------------------------------

from django import forms
from django.contrib.auth.models import User
from .models import ExternalAccount, Account

# User Registration Form
# ----------------------------------------------------
class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget = forms.PasswordInput)
    confirm = forms.CharField(widget = forms.PasswordInput, label = "Confirm password")
    
    # Meta class to specify model and fields
    # ----------------------------------------------------
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "password"]
    
    # Custom validation to check if passwords match
    # ----------------------------------------------------
    def clean(self):
        data = super().clean()
        if data.get("password") != data.get("confirm"):
            raise forms.ValidationError("Passwords do not match!")
        return data

# External Deposit/Withdrawal Form
# ----------------------------------------------------
class DepositWithdrawForm(forms.Form):
    account = forms.ChoiceField(choices = [(Account.CHECKING, "Checking"), (Account.SAVINGS, "Savings")])
    amount = forms.DecimalField(min_value = 0.01, decimal_places = 2, max_digits = 12)

# Transfer Form
# ----------------------------------------------------
class TransferForm(forms.Form):
    # Account choices for transfer
    # ----------------------------------------------------
    FROM_CHOICES = [(Account.CHECKING, "Checking"), (Account.SAVINGS, "Savings")]
    TO_CHOICES = FROM_CHOICES
    
    # Form fields
    # ----------------------------------------------------
    from_account = forms.ChoiceField(choices = FROM_CHOICES, label = "From")
    to_account = forms.ChoiceField(choices = TO_CHOICES, label = "To")
    amount = forms.DecimalField(min_value = 0.01, decimal_places = 2, max_digits = 12)
    
    # Custom validation to prevent transferring to the same account
    # ----------------------------------------------------
    def clean(self):
        data = super().clean()
        if data.get("from_account") == data.get("to_account"):
            raise forms.ValidationError("Cannot transfer to the same account!")
        return data

# External Transfer Form
# ----------------------------------------------------
class ExternalTransferForm(forms.Form):
    from_account = forms.ChoiceField(choices=[(Account.CHECKING, "Checking"), (Account.SAVINGS, "Savings")])
    amount = forms.DecimalField(min_value = 0.01, decimal_places = 2, max_digits = 12)
    external_id = forms.ModelChoiceField(queryset = ExternalAccount.objects.none(), label = "To External Account")
    
    # Initialize form with user to filter external accounts
    # ----------------------------------------------------
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['external_id'].queryset = ExternalAccount.objects.filter(user = user)
        
# External Account Form
# ----------------------------------------------------
class ExternalAccountForm(forms.ModelForm):
    
    # Meta class to specify model and fields
    # ----------------------------------------------------
    class Meta:
        model = ExternalAccount
        fields = ["bank_name", "routing_number", "account_number", "nickname"]