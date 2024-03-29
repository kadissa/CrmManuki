import datetime
import logging
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from dotenv import load_dotenv

from webhooks.models import Guest
from .models import Customer

load_dotenv()

logging.basicConfig(level=logging.DEBUG, filename='logs/bnovo_views.log',
                    filemode='a', format='%(asctime)s, %(levelname)s, '
                                         '%(message)s, %(name)s')


class TodayListView(LoginRequiredMixin, generic.ListView):
    model = Customer

    today = datetime.date.today().isoformat()
    debug_today = datetime.datetime.now().strftime('%Y-%m-%d')
    template_name = 'base.html'

    def get_queryset(self):
        today = datetime.date.today().isoformat()
        super().get_queryset()
        queryset = (Customer.objects.filter(real_arrival__contains=today) |
                    Customer.objects.filter(real_departure__contains=today))
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        today = datetime.date.today().isoformat()
        context = super(TodayListView, self).get_context_data(**kwargs)
        sauna = (Guest.objects.filter(start__contains=today).exclude(
            status='Отменено') &
                 Guest.objects.filter(start__contains=today).exclude(
                     ful_name='Уборщик'))
        context['today'] = today
        context['sauna'] = sauna
        return context


class SaunaDetailView(LoginRequiredMixin, generic.DetailView):
    model = Guest
    template_name = 'sauna.html'
    slug_field = 'id'
    context_object_name = 'sauna'


class ChaleDetailView(LoginRequiredMixin, generic.DetailView):
    model = Customer
    template_name = 'chale.html'
    slug_field = 'id'
    context_object_name = 'chale'
