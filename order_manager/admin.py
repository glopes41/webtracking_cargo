from django.contrib import admin
from order_manager.models import Client, Order
from django.contrib.sessions.models import Session


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    ordering = ('id',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'delivery_date', 'client',
                    'driver', 'status', 'last_update')
    list_display_links = ('delivery_date', 'client', 'driver')
    list_filter = ('status', 'client', 'driver')
    search_fields = ('client__name', 'driver__name')
    list_editable = ('status',)
    list_per_page = 10
    ordering = ('delivery_date',)


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ['session_key', 'expire_date', 'get_decoded_data']
    readonly_fields = ['session_data', 'expire_date', 'get_decoded_data']

    def get_decoded_data(self, obj):
        return obj.get_decoded()

    # get_decoded_data.short_description = 'Dados da Sessão'
