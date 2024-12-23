from django.urls import path
from . import views
from .views import user_login, user_logout

urlpatterns = [
    path('add-user/', views.add_user, name='add-user'),
    path('add-currency/', views.add_currency, name='add-currency'),
    path('add-transaction/', views.add_transaction, name='add-transaction'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
]
