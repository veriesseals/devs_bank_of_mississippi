from django.shortcuts import render, redirect, get_object_or_404
from decimal import Decimal
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from .models import Account, Transaction, ExternalAccount
from .forms import (
    RegisterForm, DepositWithdrawForm, TransferForm,
    ExternalTransferForm, ExternalAccountForm
)

# Create your views here.
# ----------------------------------------------------

# User Registration View
# ----------------------------------------------------
def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.save()
            login(request, user)
            messages.success(request, "Registration successful!")
            return redirect("home")
    else:
        form = RegisterForm()
    return render(request, "registration/register.html", {"form": form})


# Dashboard View
# ----------------------------------------------------
@login_required
def dashboard(request):
    checking = Account.objects.get(user = request.user, kind = Account.CHECKING)
    savings = Account.objects.get(user = request.user, kind = Account.SAVINGS)
    txs = Transaction.objects.filter(user = request.user).order_by("-created_at")[:10]
    return render(request, "dashboard.html", {"checking": checking, "savings": savings, "txs": txs})

# Deposit View
# ----------------------------------------------------
@login_required
def deposit(request):
    if request.method == "POST":
        form = DepositWithdrawForm(request.POST)
        if form.is_valid():
            account = Account.objects.get(user = request.user, kind = form.cleaned_data["account"])
            amount = form.cleaned_data["amount"]
            with transaction.atomic():
                account.balance = (acount.balance + amount).quantized(Decimal("0.01"))
                account.save()
                Transaction.objects.create(user = request.user, tx_type=Transaction.DEPOSIT, account = amount, memo = "Deposit")
            messages.success(request, "Deposit complete. Balance updated.")
            return redirect("dashboard")
    else:
        form = DepositWithdrawForm()
    return render(request, "deposit.html", {"form": form})

# Withdraw View
# ----------------------------------------------------

@login_required
def withdraw(request):
    if request.method == "POST":
        form = DepositWithdrawForm(request.POST)
        if form.is_valid():
            account = Account.objects.get(user = request.user, kind = form.cleaned_data["account"])
            amount = form.cleaned_data["amount"]
            if account.balance < amount:
                form.add_error("amount", "Insufficient funds!")
            else:
                with transaction.atomic():
                    account.balance = (account.balance - amount).quantize(Decimal("0.01"))
                    account.save()
                    Transaction.objects.create(user = request.user, tx_type=Transaction.WITHDRAW, account = amount, memo = "Withdraw")
                messages.success(request, "Withdraw complete. Balance updated.")
                return redirect("dashboard")
    else:
        form = DepositWithdrawForm()
    return render(request, "withdraw.html", {"form": form})

# Internal Transfer View
# ----------------------------------------------------

@login_required
def transfer_internal(request):
    if request.method == "POST":
        # Handle transfer form submission
        # ----------------------------------------------------
        form = TransferForm(request.POST)
        if form.is_valid():
            from_account = Account.objects.get(user = request.user, kind = form.cleaned_data["from_account"])
            to_account = Account.objects.get(user = request.user, kind = form.cleaned_data["to_account"])
            amount = form.cleaned_data["amount"]
            if from_account.balance < amount:
                form.add_error("amount", "Insufficient funds!")
            else:
                with transaction.atomic():
                    from_account.balance = (from_account.balance - amount).quantize(Decimal("0.01"))
                    to_account.balance = (to_account.balance + amount).quantize(Decimal("0.01"))
                    from_account.save()
                    to_account.save()
                    Transaction.objects.create(user = request.user, tx_type=Transaction.TRANSFER, account = from_account, amount = amount, memo = f"Transfer to {to_account.kind}")
                messages.success(request, "Transfer complete. Balances updated.")
                return redirect("dashboard")
    else:
        form = TransferForm()
    return render(request, "transfer.html", {"form": form, "title": "Transfer between your accounts"})
            

            