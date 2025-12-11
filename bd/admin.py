from django.contrib import admin
from .models import TypeA, Okrug, Address, Device

@admin.register(TypeA)
class TypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_filter = ('name',)
    search_fields = ('name',)

@admin.register(Okrug)
class OkrugAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_filter = ('name',)
    search_fields = ('name',)

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'okrug')
    list_filter = ('adr_id', 'name', 'okrug')
    search_fields = ('adr_id', 'name')

@admin.register(Device)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('id', 'ip')
    list_filter = ('ip',)
    search_fields = ('ip',)

