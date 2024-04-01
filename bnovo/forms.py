from .models import Customer
from django import forms
from django.forms import CharField


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'


class CustomerEditForm(forms.ModelForm):
    # fields = ('prepayment', 'birch_broom', 'oak_broom', 'bed_sheet', 'towel',
    #           'robe', 'slippers')

    prepayment = CharField(label='Предоплата', required=False)
    rotenburo = CharField()
    birch_broom = CharField(label='Веник берёза', required=False)
    oak_broom = CharField(label='Веник дуб', required=False)
    bed_sheet = CharField(label='Простыня', required=False)
    towel = CharField(label='Полотенце', required=False)
    robe = CharField(label='Халат', required=False)
    slippers = CharField(label='Тапки', required=False)
