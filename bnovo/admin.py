from django.contrib import admin
from .models import Customer


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('booking_id', 'full_name', 'phone',
                    # 'email',
                    'source',
                    'real_arrival',
                    'real_departure',
                    'colored_name', 'tag',)
    list_display_links = ('full_name',)
    fields = ('booking_id', 'phone', 'full_name', 'real_arrival',
              'real_departure', 'email', 'adults',
              'source', 'tag')
    readonly_fields = (
        'booking_id',
        'full_name',
        'real_arrival',
        'real_departure',
        'email',
        'adults',
        'source',
    )
    list_editable = ('tag',)
    list_filter = ['source']
    empty_value_display = '-пусто-'
    search_fields = ('full_name',)
