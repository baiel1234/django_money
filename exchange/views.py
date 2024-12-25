from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import User, Currency, Transaction,Report
from .serializers import UserSerializer, CurrencySerializer, TransactionSerializer,ReportSerializer
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
import json
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.serializers import ModelSerializer
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticated
from django.db.models.signals import post_save
from django.dispatch import receiver

@api_view(['POST'])
def add_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "User created successfully!"})
    return Response(serializer.errors)

@api_view(['POST'])
def add_currency(request):
    serializer = CurrencySerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Currency added successfully!"})
    return Response(serializer.errors)

@api_view(['POST'])
def add_transaction(request):
    serializer = TransactionSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Transaction added successfully!"})
    return Response(serializer.errors)

@api_view(['POST'])
def user_login(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)  # Загружаем JSON-данные
            username = data.get('username')
            password = data.get('password')

            if not username or not password:
                return JsonResponse({"error": "Username and password are required"}, status=400)

            user = authenticate(request, username=username, password=password)

            if user is not None:
                if user.is_active:  # Проверяем, что пользователь активен
                    login(request, user)
                    return JsonResponse({"message": "Login successful"})
                else:
                    return JsonResponse({"error": "Account is disabled"}, status=403)
            else:
                return JsonResponse({"error": "Invalid username or password"}, status=400)

        except json.JSONDecodeError:  # Обработка ошибки JSON
            return JsonResponse({"error": "Invalid JSON format"}, status=400)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)

def user_logout(request):
    logout(request)
    return JsonResponse({'message': 'Logout successful'})

class TransactionListView(generics.ListAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['currency']  # Фильтрация по валюте

# Serializer for User
class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

# ViewSet for User
class UserViewSet(ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# ViewSet for Currency
class CurrencyViewSet(ReadOnlyModelViewSet):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer

# ViewSet for Transaction
class TransactionViewSet(ReadOnlyModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

@receiver(post_save, sender=Transaction)
def update_report(sender, instance, **kwargs):
    currency = instance.currency
    report, created = Report.objects.get_or_create(currency=currency)

    if instance.type == 'buy':  # Покупка
        report.total_bought += instance.quantity
        report.total_spent_on_buy += instance.total
    elif instance.type == 'sell':  # Продажа
        report.total_sold += instance.quantity
        report.total_earned_on_sell += instance.total

    report.update_net_profit()

class ReportViewSet(ReadOnlyModelViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer