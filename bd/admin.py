from django.contrib import admin
from .models import TypeA, Okrug, Address, Device

@admin.register(TypeA)
class TypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

@admin.register(Okrug)
class OkrugAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'okrug')

@admin.register(Device)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('id', 'ip')

