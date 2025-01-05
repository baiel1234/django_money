from rest_framework import generics,viewsets, status
from rest_framework.serializers import ModelSerializer
from rest_framework.viewsets import ReadOnlyModelViewSet,GenericViewSet
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.mixins import DestroyModelMixin,CreateModelMixin, ListModelMixin, RetrieveModelMixin,UpdateModelMixin 
from .models import User, Currency, Transaction,Report
from .serializers import UserSerializer, CurrencySerializer, TransactionSerializer,ReportSerializer
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.hashers import check_password
from django_filters.rest_framework import DjangoFilterBackend
import json


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

@api_view(['GET'])
def filter_transactions(request):
    # Получаем параметры из запроса
    currency_id = request.GET.get('currency')  # ID валюты
    transaction_type = request.GET.get('type')  # 'buy' или 'sell'

    # Базовый queryset
    transactions = Transaction.objects.all()

    # Фильтрация по валюте
    if currency_id:
        try:
            transactions = transactions.filter(currency_id=currency_id)
        except Exception as e:
            return Response({"error": f"Invalid currency filter: {str(e)}"}, status=400)

    # Фильтрация по типу транзакции
    if transaction_type:
        if transaction_type in ['buy', 'sell']:
            transactions = transactions.filter(type=transaction_type)
        else:
            return Response({"error": "Invalid transaction type"}, status=400)

    # Сериализация результатов
    serializer = TransactionSerializer(transactions, many=True)
    return Response(serializer.data)

@api_view(['DELETE'])
def delete_all_transactions(request):
    """
    Удаление всех транзакций из базы данных.
    """
    try:
        # Удаляем все записи из модели Transaction
        Transaction.objects.all().delete()
        return Response({"message": "All transactions have been deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def user_login(request):
    """
    Авторизация пользователя
    """
    data = request.data
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return Response({"error": "Username and password are required"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.get(username=username)
        if check_password(password, user.password):  # Проверка пароля
            return Response({"message": "Login successful", "user_id": user.id}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

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
class CurrencyViewSet(DestroyModelMixin, viewsets.ReadOnlyModelViewSet):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer

# ViewSet for Transaction
class TransactionViewSet(UpdateModelMixin ,CreateModelMixin, ListModelMixin, RetrieveModelMixin, GenericViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    def create(self, request, *args, **kwargs):
        # Получаем данные из запроса
        data = request.data

        # Исключаем валюту "Som"
        try:
            currency = Currency.objects.get(pk=data['currency'])
            if currency.name == "Som":
                return Response({"error": "Cannot create transactions with 'Som' currency"}, status=status.HTTP_400_BAD_REQUEST)
        except Currency.DoesNotExist:
            return Response({"error": "Currency not found"}, status=status.HTTP_404_NOT_FOUND)

        # Валидация и сохранение
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    # PUT/PATCH: Обновление транзакции
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    # DELETE: Удаление транзакции
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message": "Transaction deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        # Реализация удаления объекта
        instance.delete()

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

u