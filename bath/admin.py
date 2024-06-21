from django.contrib import admin

from bath.models import (Appointment, Customer, Product, AppointmentItem,
                         Rotenburo)


class AppointmentAdminInline(admin.TabularInline):
    model = Appointment


class CustomerAdminInline(admin.TabularInline):
    model = Customer


class RotenburoAdminInline(admin.TabularInline):
    model = Rotenburo


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'quantity', 'price')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'surname',
        'email',
        'phone',
    )
    inlines = [AppointmentAdminInline]


class AppointmentItemInline(admin.TabularInline):
    model = AppointmentItem
    raw_id_fields = ['product']


@admin.register(AppointmentItem)
class AppointmentItemAdmin(admin.ModelAdmin):
    list_display = (
        'appointment',
        'product',
        'price',
        'total_price',
        'quantity',
    )


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'customer',
        'date',
        'start_time',
        'end_time',
        'price',
        'services_price',
    )
    search_fields = ('start_time',)
    inlines = [AppointmentItemInline, RotenburoAdminInline]


@admin.register(Rotenburo)
class RotenburoAdmin(admin.ModelAdmin):
    list_display = (
        'appointment',
        'start_time',
        'end_time',
        'amount',
        'price',
    )
