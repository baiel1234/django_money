from django.contrib import admin
from .models import User, Currency, Transaction

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username')
    search_fields = ('username',)
    ordering = ('id',)

@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name','quantity')
    search_fields = ('name',)
    ordering = ('id',)

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('type', 'currency', 'quantity', 'rate', 'total', 'timestamp')
    readonly_fields = ('total',)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "currency":
            kwargs["queryset"] = Currency.objects.excluding_som()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)