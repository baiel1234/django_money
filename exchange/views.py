from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import User, Currency, Transaction
from .serializers import UserSerializer, CurrencySerializer, TransactionSerializer
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
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
