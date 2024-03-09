import csv
import json
import threading
from secrets import compare_digest

from django.db.transaction import non_atomic_requests
from django.http import HttpResponse, HttpResponseForbidden
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from webhooks.api_connect import *
from webhooks.models import WebhookData, Customer

WEBHOOK_TOKEN = os.getenv('WEBHOOK_TOKEN')
TITLES_CSV = [
    'id', 'Статус бронирования', 'Начало бронирования',
    'Конец бронирования', 'Продолжительность', 'Стоимость заказа',
    'Источник бронирования', 'Телефон клиента',
    'email клиента', 'Полное имя', 'Комментарий к заказу'
]


def get_cleaned_data(data):
    cleaned_data = {
        'booking_id': data.get('id'),
        'status': data.get('booking_status'),
        'start': data.get('booking_date_start_formatted'),
        'end': data.get('booking_date_end_formatted'),
        'duration': data.get('booking_duration_formatted'),
        'price': data.get('booking_price_formatted'),
        'source': data.get('booking_source'),
        'phone': data.get('customer_phone'),
        'email': data.get('customer_email'),
        'ful_name': data.get('customer_full_name'),
        'comment': data.get('customer_comment')
    }
    return cleaned_data


@csrf_exempt
@require_POST
@non_atomic_requests
def easyweek_hook(request):
    webhook_token = request.headers.get('Webhook-Token', 'Empty string!')
    if not compare_digest(webhook_token, WEBHOOK_TOKEN):
        return HttpResponseForbidden(
            "Incorrect token in Webhook-Token header.",
            content_type="text/plain",
        )
    request_body = request.body
    payload: dict = json.loads(request_body.decode('utf-8'))
    WebhookData.objects.create(
        received_at=timezone.now(),
        payload=payload,
    )
    status = payload.get('booking_status')
    customer_email = payload.get('customer_email')
    end_booking = payload.get('booking_date_end_formatted').split()[-1]
    Customer.objects.create(**get_cleaned_data(payload)
                            )
    with open('booking_data.csv', 'a+', encoding='utf-8') as file:
        file_writer = csv.writer(file, delimiter=',', lineterminator='\r\n')
        # file_writer.writerow(TITLES_CSV)
        file_writer.writerow(
            [get_cleaned_data(payload).get(key) for key in
             get_cleaned_data(payload)]
        )
    if (status == 'Новое бронирование' and customer_email !=
            'cleaning@clean.ru' and end_booking != '23:00'):
        threading.Thread(
            target=create_booking, args=(session, payload)).start()
    return HttpResponse(status=200)


# @csrf_exempt
# @require_POST
# async def respond(request):
#     webhook_token = request.headers.get('Webhook-Token', 'Empty string')
#     if not compare_digest(webhook_token, WEBHOOK_TOKEN):
#         return HttpResponseForbidden(
#             "Incorrect token in Webhook-Token header.",
#             content_type="text/plain",
#         )
#     request_data = request.body
#     request_headers = request.headers
#     print(request_headers)
#     decoded_data: dict = json.loads(request_data.decode('utf-8'))
#     booking = {'id': decoded_data.get('id'),
#                'booking_status': decoded_data.get('booking_status'),
#                'booking_start': decoded_data.get('booking_date_start_formatted'
#                                                  ),
#                'booking_end_': decoded_data.get('booking_date_end_formatted'),
#                'duration': decoded_data.get(
#                    'booking_duration_formatted'),
#                'booking_price': decoded_data.get('booking_price_formatted'),
#                'booking_source': decoded_data.get('booking_source'),
#                'customer_phone': decoded_data.get('customer_phone'),
#                'customer_email': decoded_data.get('customer_email'),
#                'customer_full_name': decoded_data.get('customer_full_name'),
#                'customer_comment': decoded_data.get('customer_comment'),
#
#                }
#     with open('booking_data.csv', 'a+', encoding='utf-8') as file:
#         file_writer = csv.writer(file, delimiter=',', lineterminator='\r\n')
#         # file_writer.writerow(TITLES_CSV)
#         file_writer.writerow([booking.get(key) for key in booking])
#     status = decoded_data.get('booking_status')
#     end_booking = decoded_data.get('booking_date_end_formatted').split()[-1]
#     customer_email = decoded_data.get('customer_email')
#     book_id = decoded_data.get('id')
#     print(f'Статус={status}')
#     print(f'end_booking = {end_booking}')
#     print(f'book_id = {book_id}')
#     if (status == 'Новое бронирование' and customer_email !=
#             'cleaning@clean.ru' and end_booking != '23:00'):
#         threading.Thread(
#             target=create_booking, args=(session, decoded_data)).start()
#     pprint(decoded_data)
#     return HttpResponse(status=200)
