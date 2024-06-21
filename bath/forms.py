from django import forms

from .models import Appointment, Customer


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = (
            'date',
            'start_time',
            'end_time',
        )


class CustomerForm(forms.ModelForm):
    email = forms.EmailField(
        widget=forms.TextInput(attrs={'placeholder': 'Email'}), label='')
    phone = forms.IntegerField(
        widget=forms.TextInput(attrs={'placeholder': 'Телефон'}),
        label='',
        error_messages={'error': 'Введите цифры'})

    class Meta:
        model = Customer
        fields = ('email', 'name', 'phone')
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Имя'}),
            # 'phone': forms.TextInput(attrs={'placeholder': 'Телефон'})
        }
        labels = {'name': '', 'email': '', 'phone': ''}


class CartAddProductForm(forms.Form):
    quantity = forms.IntegerField(label='', required=False,
                                  widget=forms.TextInput(attrs={
                                      'placeholder': 'шт.'}))
