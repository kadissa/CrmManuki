from django.db import models


# Create your models here.
class WebhookData(models.Model):
    received_at = models.DateTimeField(help_text="Время получения веб-хука.")
    payload = models.JSONField(default=None, null=True)

    class Meta:
        indexes = [
            models.Index(fields=["received_at"]),
        ]


class Customer(models.Model):
    booking_id = models.CharField(max_length=60, db_index=True)
    status = models.CharField('Статус бронирования', max_length=60)
    start = models.CharField('Начало бронирования', max_length=60)
    end = models.CharField('Конец бронирования', max_length=60)
    duration = models.CharField('Продолжительность', max_length=60)
    price = models.CharField('Стоимость заказа', max_length=60)
    source = models.CharField('Источник бронирования', max_length=60)
    phone = models.CharField('Телефон клиента', max_length=60)
    email = models.CharField(max_length=60)
    ful_name = models.CharField('Полное имя', max_length=60)
    comment = models.CharField('Комментарий к заказу', max_length=60)

    class Meta:
        verbose_name = 'Гость'
        verbose_name_plural = 'Гости'
        constraints = [models.UniqueConstraint(
            fields=['booking_id', 'status'], name='unique_booking_id_status')]

    def __str__(self):
        return self.email
