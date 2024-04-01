import datetime
import logging
import os

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.db.models import signals
from django.dispatch import receiver
from django.views import generic
from dotenv import load_dotenv

from webhooks.models import Guest
from .models import Customer
from django.contrib.auth import get_user, get_user_model
load_dotenv()

logging.basicConfig(level=logging.DEBUG, filename='logs/bnovo_views.log',
                    filemode='a', format='%(asctime)s, %(levelname)s, '
                                         '%(message)s, %(name)s')


class TodayListView(LoginRequiredMixin, generic.ListView):
    model = Customer
    today = datetime.date.today().isoformat()
    debug_today = datetime.datetime.now().strftime('%Y-%m-%d')
    template_name = 'index.html'

    def get_queryset(self):
        if self.kwargs:
            delta = self.kwargs['date']
        else:
            delta = 0
        any_day = datetime.date.today() + datetime.timedelta(days=int(delta))

        today = any_day.isoformat()
        super().get_queryset()
        queryset = (Customer.objects.filter(real_arrival__contains=today) |
                    Customer.objects.filter(real_departure__contains=today))
        print()
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        if self.kwargs:
            delta = self.kwargs['date']
        else:
            delta = 0
        any_day = datetime.date.today() + datetime.timedelta(days=int(delta))
        today = any_day.isoformat()
        context = super(TodayListView, self).get_context_data(**kwargs)
        sauna = (Guest.objects.filter(start__contains=today).exclude(
            status='Отменено') &
                 Guest.objects.filter(start__contains=today).exclude(
                     ful_name='Уборщик'))
        context['today'] = today
        context['sauna'] = sauna
        context['delta'] = delta

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


class ChaleDetailCreateView(LoginRequiredMixin, generic.CreateView):
    form = ''


@receiver(signals.post_save, sender=Customer)
def check_about_black_list(sender, **kwargs):
    """Ищет в базе объект с тегом 'black-list', сравнивает его телефон с
    телефоном последней записи в базу. В случае совпадения отсылает email"""
    black_list_queryset = sender.objects.filter(tag='black-list')
    last_object = sender.objects.latest('id')
    if black_list_queryset:
        for obj in black_list_queryset:
            if last_object.phone == obj.phone:
                print(f'Гость {last_object}, с меткой <black-list> '
                      'забронировал домик на '
                      f'{last_object.real_arrival}')
                send_mail(
                    subject='Внимание!',
                    message=f'Гость {last_object}, телефон:{last_object.phone}'
                            f'с  меткой <black-list> '
                            f'забронировал домик на '
                            f'{last_object.real_arrival}',
                    from_email=os.getenv('EMAIL_HOST_USER'),
                    recipient_list=['kadissa70@gmail.com']
                )
