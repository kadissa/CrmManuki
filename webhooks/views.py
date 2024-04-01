import json
import logging
import os
import threading
from secrets import compare_digest

from django.db.transaction import non_atomic_requests
from django.http import HttpResponse, HttpResponseForbidden
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.core.mail import send_mail
from webhooks.api_connect import *
from webhooks.models import WebhookData, Guest

WEBHOOK_TOKEN = os.getenv('WEBHOOK_TOKEN_EASYWEEK')
TITLES_CSV = [
    'id', 'Статус бронирования', 'Начало бронирования',
    'Конец бронирования', 'Продолжительность', 'Стоимость заказа',
    'Источник бронирования', 'Телефон клиента',
    'email клиента', 'Полное имя', 'Комментарий к заказу'
]

logging.basicConfig(level=logging.DEBUG, filename='logs/webhooks_views.log',
                    filemode='a', format='%(asctime)s, %(levelname)s, '
                                         '%(message)s, %(name)s, %(funcName)')


def format_date(data, start_or_end):
    booking = data.get(start_or_end)
    from_iso = datetime.datetime.fromisoformat(booking)
    real_booking_time = from_iso + datetime.timedelta(hours=3)
    format_time = datetime.datetime.strftime(real_booking_time,
                                             '%Y-%m-%d %H:%M')
    logging.debug(format_time)
    return format_time


def get_cleaned_data(data):
    cleaned_data = {
        'booking_id': data.get('id'),
        'status': data.get('booking_status'),
        'start': format_date(data, 'booking_date_start'),
        'end': format_date(data, 'booking_date_end'),
        'duration': data.get('booking_duration_formatted'),
        'price': data.get('booking_price_formatted'),
        'source': data.get('booking_source'),
        'phone': data.get('customer_phone'),
        'email': data.get('customer_email'),
        'ful_name': data.get('customer_full_name'),
        'comment': data.get('customer_comment'),
        'uid': data.get('uid')
    }
    return cleaned_data


def check_black_list_tag(webhook_data):
    time.sleep(4)
    queryset_list = Guest.objects.filter(tag='black-list')
    phone = webhook_data.get('customer_phone')
    email = webhook_data.get('customer_email')
    logging.debug([obj for obj in queryset_list])
    for obj in queryset_list:
        logging.debug(f'в цикле {obj.email}, '
                      f'Email:{webhook_data.get('customer_email')}, '
                      f'Имя:{webhook_data.get('customer_full_name')}, '
                      f'Телефон:{webhook_data.get('customer_phone')}, '
                      f'obj.phone:{obj.phone}')
        if phone == obj.phone or email == obj.email:
            logging.debug(f'---{email} --{obj.email}--')
            send_mail(
                subject='Внимание',
                from_email=os.getenv('EMAIL_HOST_USER'),
                message=f'Гость {obj.ful_name} с меткой '
                        'black-list забронировал баню на '
                        f'{webhook_data.get("booking_date_start")}',
                recipient_list=['kadissa70@gmail.com']
            )
            logging.info('письмо отправлено')


@csrf_exempt
@require_POST
@non_atomic_requests
def easyweek_hook(request):
    webhook_token = request.headers.get('Webhook-Token', 'Empty string!')
    if not compare_digest(webhook_token, WEBHOOK_TOKEN):
        logging.error('Incorrect token in Webhook-Token header.')
        return HttpResponseForbidden(
            "Incorrect token in Webhook-Token header.",
            content_type="text/plain",
        )
    request_body = request.body
    payload: dict = json.loads(request_body.decode('utf-8'))
    logging.debug(f'длина словаря payload: {len(payload)}')
    WebhookData.objects.create(
        received_at=timezone.now(),
        payload=payload,
    )
    booking_id = payload.get('id')
    end = format_date(payload, 'booking_date_end')
    status = payload.get('booking_status')
    customer_name = payload.get('customer_name')
    end_booking = payload.get('booking_date_end_formatted').split()[-1]
    logging.info(f'статус:{status}, '
                 f'customer_name:{customer_name}, '
                 f'end_booking:{end_booking}')
    threading.Thread(target=check_black_list_tag, args=(payload,)).start()
    Guest.objects.update_or_create(booking_id=booking_id,
                                   defaults=get_cleaned_data(payload))
    if (status == 'Новое бронирование' and
            customer_name != 'Уборщик'
            and end_booking != '23:00'):
        threading.Thread(
            target=create_booking, args=(session, payload)).start()
    if status == 'Отменено' and customer_name != 'Уборщик':
        if Guest.objects.filter(start=end).exists():
            cleaner = Guest.objects.get(start=end)
            logging.debug(f'cleaner: {cleaner.ful_name}')
            if cleaner.ful_name == 'Уборщик':
                threading.Thread(target=cancel_booking,
                                 args=(session, cleaner.uid)).start()
        else:
            logging.error('Не отменился уборщик.')
    return HttpResponse(status=200)
