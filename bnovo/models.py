import django.utils.timezone
from django.contrib import admin
from django.db import models
from django.utils.html import format_html


class Customer(models.Model):
    booking_id = models.CharField(max_length=20, db_index=True, unique=True)
    phone = models.CharField('Телефон', max_length=20, null=True)
    full_name = models.CharField('Имя', max_length=100)
    date = models.CharField('Дата', max_length=20)
    real_arrival = models.CharField('Время заезда', max_length=40)
    real_departure = models.CharField('Время выезда', max_length=40)
    room_id = models.CharField('Номер Домика', max_length=40, null=True)
    adults = models.CharField('Взрослых', max_length=20, null=True)
    children = models.CharField('Детей', max_length=20, null=True)
    email = models.CharField(max_length=128, null=True)
    source = models.CharField('Источник бронирования', max_length=200)
    tag = models.CharField('Примечание', max_length=200, blank=True, null=True)
    timestamp = models.DateTimeField(default=django.utils.timezone.now)
    amount = models.CharField('Проживание', max_length=50, null=True)
    payment = models.CharField(max_length=50, null=True)
    service_total = models.CharField('', max_length=256, null=True)
    status_name = models.CharField('', max_length=256, null=True)
    is_early_arrival = models.CharField('', max_length=256, null=True)
    is_late_departure = models.CharField('', max_length=256, null=True)
    need_online_payment = models.CharField('', max_length=256, null=True)

    @admin.display(ordering='booking_id')
    def colored_name(self):
        return format_html(
            '<span style="color: #{};">{} {}</span>',
            self.booking_id,
            self.full_name,
            self.email,
        )

    colored_name.short_description = 'Имя Email'

    # colored_name.admin_order_field = 'full_name'
    class Meta:
        verbose_name = 'Гость'
        verbose_name_plural = 'Гости'
        # constraints = [models.UniqueConstraint(
        #     fields=['booking_id', 'phone'], name='unique_phone_booking_id')]

    def __str__(self):
        return self.full_name
