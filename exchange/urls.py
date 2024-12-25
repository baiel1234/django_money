from django.urls import path,include
from . import views
from .views import user_login, user_logout,UserViewSet ,CurrencyViewSet, TransactionViewSet,ReportViewSet
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
    path('add-transaction/', views.add_transaction, name='add-transaction'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('', include(router.urls)),
]
