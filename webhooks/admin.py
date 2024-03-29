from django.contrib import admin
from django.contrib.admin import ModelAdmin
from webhooks.models import Guest, WebhookData


@admin.register(Guest)
class CustomerAdmin(ModelAdmin):
    ordering = ('-booking_id',)
    list_display_links = ('ful_name',)
    # view_on_site = False
    #
    # def view_on_site(self, obj):
    #     url = reverse("person-detail", kwargs={"slug": obj.slug})
    #     return "https://example.com" + url
    list_display = (
        'uid',
        'ful_name',
        'phone',
        'booking_id',
        'status',
        'start',
        'end',
        'duration',
        'source',
        'email',
        'comment',
        'tag',
    )
    fields = [
        # 'booking_id',
        # 'uid',
        'status',
        ('start', 'end'),
        'duration',
        'price',
        'source',
        'phone',
        'email',
        'ful_name',
        'comment',
        'people_count',
        'prepayment',
        'rotenburo',
        'birch_broom',
        'oak_broom',
        'bed_sheet',
        'towel',
        'robe',
        'slippers',
        'tag',
    ]
    readonly_fields = (
        'uid',
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
    list_editable = ('tag',)
    search_fields = ('email', 'ful_name',)
    list_filter = ('phone',)
    empty_value_display = '-пусто-'

