from django.contrib import admin
from django.contrib.admin import ModelAdmin
from webhooks.models import Customer


@admin.register(Customer)
class CustomerAdmin(ModelAdmin):
    # view_on_site = False
    #
    # def view_on_site(self, obj):
    #     url = reverse("person-detail", kwargs={"slug": obj.slug})
    #     return "https://example.com" + url
    list_display = (
        'pk',
        'booking_id',
        'status',
        'start',
        # 'end',
        'duration',
        # 'price',
        'source',
        'phone',
        'email',
        'ful_name',
        'comment',
    )
    fields = (
        'booking_id',
        'status',
        'start',
        'end',
        'duration',
        'price',
        'source',
        'phone',
        'email',
        'ful_name',
        'comment',
    )
    readonly_fields = (
        'booking_id',
        'status',
        'start',
        'end',
        'duration',
        'price',
        'source',
        'phone',
        'email',
        'ful_name',
        'comment',
    )
    search_fields = ('email',)
    list_filter = ('phone',)
    empty_value_display = '-пусто-'
