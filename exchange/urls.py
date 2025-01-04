from django.urls import path,include
from . import views
from .views import user_login,delete_all_transactions,filter_transactions, user_logout,UserViewSet ,CurrencyViewSet, TransactionViewSet,ReportViewSet
from rest_framework.routers import DefaultRouter

# Router configuration
router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'currencies', CurrencyViewSet, basename='currency')
router.register(r'transactions', TransactionViewSet, basename='transaction')
router.register(r'reports', ReportViewSet, basename='report')


urlpatterns = [
    path('add-user/', views.add_user, name='add-user'),
    path('add-currency/', views.add_currency, name='add-currency'),
    path('login/', user_login, name='user_login'),    path('transactions/filter/', filter_transactions, name='filter_transactions'),
    path('transactions/delete-all/', delete_all_transactions, name='delete_all_transactions'),
    path('', include(router.urls)),
]
  