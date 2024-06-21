# from django.db import models
# from django.urls import reverse


# Create your models here.
# class WebhookData(models.Model):
#     received_at = models.DateTimeField(help_text="Время получения веб-хука.")
#     payload = models.JSONField(default=None, null=True)
#
#     class Meta:
#         indexes = [
#             models.Index(fields=["received_at"]),
#         ]


# class Guest(models.Model):
#     booking_id = models.CharField(max_length=60, db_index=True)
#     status = models.CharField('Статус', max_length=60)
#     start = models.CharField('Начало', max_length=60)
#     end = models.CharField('Конец', max_length=60)
#     duration = models.CharField('Время', max_length=60)
#     price = models.CharField('Стоимость заказа', max_length=60)
#     price_formatted = models.CharField('Стоимость заказа',
#                                        max_length=60, null=True)
#     amount = models.CharField('Внесено', max_length=50, null=True)
#     source = models.CharField('Источник', max_length=60)
#     phone = models.CharField('Телефон', max_length=60)
#     email = models.CharField(max_length=60)
#     ful_name = models.CharField('Полное имя', max_length=60)
#     comment = models.CharField('Комментарий', max_length=60)
#     tag = models.CharField('Примечание', max_length=200, blank=True, null=True)
#
#     uid = models.CharField('booking_uuid', max_length=256, null=True)
#     people_count = models.PositiveSmallIntegerField('Кол-во чел.',
#                                                     blank=True, null=True)
#     prepayment = models.PositiveSmallIntegerField('Предоплата', blank=True,
#                                                   null=True)
#     rotenburo = models.BooleanField('Ротэнбуро', blank=True, null=True,
#                                     default=False)
#     birch_broom = models.PositiveSmallIntegerField('Веник бер.', blank=True,
#                                                    null=True)
#     oak_broom = models.PositiveSmallIntegerField('Веник дуб', blank=True,
#                                                  null=True)
#     bed_sheet = models.PositiveSmallIntegerField('Простыня', blank=True,
#                                                  null=True)
#     towel = models.PositiveSmallIntegerField('Полотенце', blank=True,
#                                              null=True)
#     robe = models.PositiveSmallIntegerField('Халат', blank=True, null=True)
#     slippers = models.PositiveSmallIntegerField('Тапки', blank=True, null=True)
#     rotenburo_1 = models.PositiveSmallIntegerField('Ротенбуро', null=True,
#                                                    blank=True)
#
#     class Meta:
#         verbose_name = 'Гость'
#         verbose_name_plural = 'Гости'
#         constraints = [models.UniqueConstraint(
#             fields=['booking_id', 'status'], name='unique_booking_id_status')]
#
#     def __str__(self):
#         return self.email
#
#     def get_absolute_url(self):
#         return reverse('bnovo:sauna_detail', kwargs={'pk': self.id})


# class Item(models.Model):
#     text = models.CharField('Резерв', max_length=200, blank=True, null=True)
#     base_sauna_price = models.PositiveSmallIntegerField('Цена бани',
#                                                         blank=True, null=True)
#     rotenburo = models.PositiveSmallIntegerField('Ротэнбуро', blank=True,
#                                                  null=True, )
#     birch_broom = models.PositiveSmallIntegerField('Веник бер.', blank=True,
#                                                    null=True)
#     oak_broom = models.PositiveSmallIntegerField('Веник дуб', blank=True,
#                                                  null=True)
#     bed_sheet = models.PositiveSmallIntegerField('Простыня', blank=True,
#                                                  null=True)
#     towel = models.PositiveSmallIntegerField('Полотенце', blank=True,
#                                              null=True)
#     robe = models.PositiveSmallIntegerField('Халат', blank=True, null=True)
#     slippers = models.PositiveSmallIntegerField('Тапки', blank=True, null=True)
#     guest_id = models.ForeignKey(Guest, on_delete=models.CASCADE,
#                                  related_name='items')
#     time_stamp = models.DateTimeField('Дата создания', auto_now_add=True,
#                                       null=True)
#
#     @property
#     def total_accessories_price(self):
#         price = (self.rotenburo + self.birch_broom + self.oak_broom +
#                  self.bed_sheet + self.towel + self.robe + self.slippers)
#         return price
#
#     @property
#     def total_price(self):
#         price = self.base_sauna_price + self.total_accessories_price
#         return price
