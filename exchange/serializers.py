from rest_framework import serializers
from .models import Currency, Transaction
from django.contrib.auth.models import User
from rest_framework.serializers import ModelSerializer
from .models import Report

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password']

class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = ['id', 'name', 'quantity']

    def validate_name(self, value):
        if Currency.objects.filter(name=value).exists():
            raise serializers.ValidationError("Currency with this name already exists.")
        return value

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id', 'type', 'currency', 'quantity', 'rate', 'total', 'timestamp']
        read_only_fields = ['total']

class ReportSerializer(ModelSerializer):
    class Meta:
        model = Report
        fields = ['currency', 'total_bought', 'total_spent_on_buy', 'total_sold', 'total_earned_on_sell', 'net_profit']