# 6) URLs (the site map)
# ----------------------------------------------------
from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),

    # auth-related pages you built
    path("register/", views.register, name="register"),

    # money actions
    path("deposit/", views.deposit, name="deposit"),
    path("withdraw/", views.withdraw, name="withdraw"),
    path("transfer/", views.transfer, name="transfer"),

    # external accounts & transfers
    path("external/", views.ext_accounts, name="ext-accounts"),
    path("external/transfer/", views.external_transfer, name="transfer-external"),
]