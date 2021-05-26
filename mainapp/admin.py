from django.contrib import admin
from .models import *

@admin.register(station_model)
class station_list(admin.ModelAdmin):
    list_display = ('name', 'is_delete')

@admin.register(bus_model)
class bus_list(admin.ModelAdmin):
    list_display = ('gos_number', 'marka', 'place_count', 'is_delete')

@admin.register(flight_model)
class flight_list(admin.ModelAdmin):
    list_display = ('bus_id', 'start_id', 'finish_id', 'date_start', 'date_finish', 'voditel_id', 'price', 'is_delete')

@admin.register(ticket_model)
class ticket_list(admin.ModelAdmin):
    list_display = ('flight_id', 'cashier_id', 'place', 'buy_time', 'is_buy', 'is_pay')