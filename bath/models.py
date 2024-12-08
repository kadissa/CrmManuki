from django.core.validators import MinValueValidator, EmailValidator
from django.db import models


class Customer(models.Model):
    name = models.CharField("Имя", max_length=60)
    surname = models.CharField("Фамилия", max_length=50, blank=True, null=True)
    email = models.EmailField(
        max_length=60, validators=[EmailValidator()], blank=True, null=True
    )
    phone = models.CharField("Телефон", max_length=15)

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField("Название", max_length=60)
    quantity = models.PositiveIntegerField("Количество", null=True, blank=True)
    price = models.PositiveSmallIntegerField("Цена", blank=True, null=True)
    slug = models.SlugField(max_length=60, db_index=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.name)

    class Meta:
        ordering = ("id",)
        index_together = (("name", "slug"),)
        verbose_name = "Аксессуар"
        verbose_name_plural = "Аксессуары"


class Appointment(models.Model):
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, verbose_name="Гость"
    )
    status = models.CharField("Статус", max_length=60, blank=True, null=True)
    date = models.DateField()
    start_time = models.TimeField("Начало")
    end_time = models.TimeField("Конец")
    duration = models.CharField("Продолжительность", max_length=60, blank=True)
    price = models.PositiveSmallIntegerField("Стоимость бани")
    services_price = models.PositiveIntegerField("Цена услуг", default=0)
    full_price = models.PositiveIntegerField("Стоимость заказа")
    amount = models.PositiveSmallIntegerField(
        "Количество часов", blank=True, null=True, validators=[MinValueValidator(2)]
    )
    source = models.CharField("Источник", max_length=60, blank=True, null=True)
    full_name = models.CharField("Полное имя", max_length=60, blank=True, null=True)
    comment = models.CharField("Комментарий", max_length=60, blank=True, null=True)
    tag = models.CharField("Примечание", max_length=200, blank=True, null=True)
    people_count = models.PositiveSmallIntegerField(
        "Кол-во чел.", blank=True, null=True
    )
    prepayment = models.PositiveSmallIntegerField("Предоплата", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Запись"
        verbose_name_plural = "Бронирования"

    def __str__(self):
        return f"Запись  {self.date} {self.start_time}-{self.end_time}"

    def save(self, *args, **kwargs):
        self.full_price = self.price + self.services_price
        super().save(*args, **kwargs)


class AppointmentItem(models.Model):
    appointment = models.ForeignKey(
        Appointment,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Заказ",
        related_name="items",
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        null=True,
        related_name="appointment_items",
    )
    price = models.CharField("цена", max_length=50)
    total_price = models.PositiveIntegerField("Стоимость", blank=True, null=True)
    quantity = models.CharField("количество", max_length=15, null=True, blank=True)

    def save(self, *args, **kwargs):
        self.total_price = int(self.price) * int((self.quantity or 0))
        super().save(*args, **kwargs)

    def get_cost(self):
        return int(self.price) * int(self.quantity or 0)

    class Meta:
        verbose_name = "Услуга в заказе"
        verbose_name_plural = "Услуги в заказе"


class Rotenburo(models.Model):
    appointment = models.ForeignKey(
        Appointment,
        on_delete=models.CASCADE,
        verbose_name="Заказ",
        related_name="rotenburos",
    )
    start_time = models.CharField("Начало", max_length=16)
    end_time = models.CharField("Конец", max_length=16)
    amount = models.PositiveIntegerField("Количество часов")
    price = models.PositiveIntegerField("Стоимость", default=0)

    def __str__(self):
        return (
            f"{self.appointment.date} - {self.appointment.start_time} - "
            f"{self.appointment.end_time}"
        )

    class Meta:
        verbose_name = "Ротенбуро"
        verbose_name_plural = "Ротенбуро"
