from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.contrib.auth.hashers import make_password

class User(models.Model):
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=150)

    def save(self, *args, **kwargs):
        if not self.password.startswith('pbkdf2_'):  # Проверка, чтобы не хешировать уже хешированные пароли
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

class CurrencyManager(models.Manager):
    def excluding_som(self):
        return self.exclude(name="Som")

class Currency(models.Model):
    name = models.CharField(max_length=50, unique=True)
    quantity = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=0.00, 
        null=True,  # Позволяет хранить NULL в базе данных
        blank=True  # Делает поле необязательным в формах, включая админку
    )

    objects = CurrencyManager()

    def __str__(self):
        return self.name

class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('buy', 'Покупка'),
        ('sell', 'Продажа'),
    ]

    type = models.CharField(max_length=4, choices=TRANSACTION_TYPES)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    rate = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=15, decimal_places=2, editable=False)  # total = rate * quantity
    timestamp = models.DateTimeField(default=now)

    def save(self, *args, **kwargs):
        # Вычисляем total перед сохранением
        self.total = self.quantity * self.rate

        # Обновляем количество валюты в зависимости от типа транзакции
        som_currency, created = Currency.objects.get_or_create(name="Som")  # Ищем или создаем валюту Som

        if self.type == 'buy':
            # При покупке: Увеличиваем количество покупаемой валюты, уменьшаем сома
            self.currency.quantity = (self.currency.quantity or 0) + self.quantity
            som_currency.quantity = (som_currency.quantity or 0) - self.total
        elif self.type == 'sell':
            # При продаже: Уменьшаем количество продаваемой валюты, увеличиваем сома
            self.currency.quantity = (self.currency.quantity or 0) - self.quantity
            som_currency.quantity = (som_currency.quantity or 0) + self.total

        self.currency.save()  # Сохраняем обновления валюты
        som_currency.save()   # Сохраняем изменения для Som
        super().save(*args, **kwargs)  # Сохраняем транзакцию

class Report(models.Model):
    currency = models.OneToOneField('Currency', on_delete=models.CASCADE, related_name='report')
    total_bought = models.DecimalField(max_digits=15, decimal_places=2, default=0)  # Сколько купили валюты
    total_spent_on_buy = models.DecimalField(max_digits=15, decimal_places=2, default=0)  # Потратили сом на покупку
    total_sold = models.DecimalField(max_digits=15, decimal_places=2, default=0)  # Сколько продали валюты
    total_earned_on_sell = models.DecimalField(max_digits=15, decimal_places=2, default=0)  # Получили сом за продажу
    net_profit = models.DecimalField(max_digits=15, decimal_places=2, default=0)  # Разница в сомах (расходы - доходы)

    def update_net_profit(self):
        self.net_profit = (self.total_earned_on_sell - self.total_spent_on_buy)
        self.save()