#  users.forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

# from webhooks.models import Guest
from django import forms
from django.forms import CharField


# class GuestSelfEditForm(forms.ModelForm):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['rotenburo_1'].label = 'Rotenburo'
#
#     def set_label_rotenburo(self, price):
#         self.fields['rotenburo_1'].label = f'Ротенбуро - {price} руб./час.'
#
#     class Meta:
#         model = Guest
#         fields = (
#             'people_count', 'rotenburo_1', 'birch_broom',
#             'oak_broom', 'bed_sheet', 'towel', 'robe', 'slippers')
#         labels = {
#             # 'rotenburo': 'Ротенбуро - 2500р/ч',
#             'oak_broom': 'веник дуб - 300р.',
#             'birch_broom': 'веник берёза - 300р.',
#             'bed_sheet': 'простыня - 100р.',
#             'towel': 'полотенце - 100р.',
#             'robe': 'халат - 100р.',
#             'slippers': 'тапки - 100р.'
#         }


# class GuestLoginForm(forms.ModelForm):
#     class Meta:
#         model = Guest
#         fields = ('phone',)
