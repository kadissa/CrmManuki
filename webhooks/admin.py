from django.contrib import admin
from django.contrib.admin import ModelAdmin
from webhooks.models import Guest, WebhookData


@admin.register(Guest)
class CustomerAdmin(ModelAdmin):
    # def get_exclude(self, request, obj=None):
    #     excluded = super().get_exclude(request,
    #                                    obj) or []  # get overall excluded fields
    #
    #     if not request.user.is_superuser:  # if user is not a superuser
    #         return excluded + ['extra_field_to_exclude']
    #
    #     return excluded  # otherwise return the default excluded fields if any

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """Limit choices for 'picture' field to only your pictures."""
        if db_field.ful_name == 'Уборщик':
            if not request.user.is_superuser:
                kwargs["queryset"] = Guest.objects.filter(
                    owner=request.user)
        return super().formfield_for_foreignkey(
            db_field, request, **kwargs)

    def get_queryset(self, request):
        """Limit Pages to those that belong to the request's user."""
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        else:
            qs = Guest.objects.exclude(ful_name='Уборщик')
            return qs


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
        # 'start',
        # 'end',
        # 'duration',
        'price',
        'source',
        # 'phone',
        'email',
        # 'ful_name',
        'comment',
    )
    list_editable = ('tag',)
    search_fields = ('email', 'ful_name',)
    list_filter = ('phone', 'ful_name')
    empty_value_display = '-пусто-'

