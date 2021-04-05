from django.urls import path, include
from api import views
from rest_framework.routers import DefaultRouter
from rest_framework.documentation import include_docs_urls


router = DefaultRouter()
router.register('users', views.CreateUser, basename="create_user")
router.register('wallets', views.WalletViewSet, basename="create_wallet")
router.register('transactions', views.TransactionViewSet, basename="transactions")
router.register('statistics', views.StatisticsViewSet, basename="statistics")

urlpatterns = [
    path('', include_docs_urls(title='Wallet API Documentation', public=False)),
]

urlpatterns += router.urls


