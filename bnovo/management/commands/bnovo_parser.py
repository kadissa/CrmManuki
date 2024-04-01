import datetime
import os
import time
import logging
from pprint import pprint
from django.core.mail import send_mail
import requests
from django.core.management.base import BaseCommand, CommandError
from bnovo.models import Customer
from webhooks.models import Guest

logging.basicConfig(level=logging.DEBUG, filename='logs/bnovo_parser.log',
                    filemode='a', format='%(asctime)s, %(levelname)s, '
                                         '%(message)s, %(name)s, %(funcName)s')
BASE_URL = 'https://online.bnovo.ru'
LOGIN = os.getenv('BNOVO_API_LOGIN')
PASSWORD = os.getenv('BNOVO_API_PASSWORD')
session = requests.Session()

HEADERS = {
    'username': LOGIN,
    'password': PASSWORD
}

response = session.post(BASE_URL, data=HEADERS)


# '875458'  шале с видом на сад
# '875457'  шале с камином
# room_type = session.get(BASE_URL + '/roomTypes/get',
#                         headers={'Accept': 'application/json'})
# room = session.get(BASE_URL + '/room',
#                    headers={'Accept': 'application/json'})
# tariff = session.get(BASE_URL + '/tariff/tariffs',
#                      headers={'Accept': 'application/json'})


def get_all_booking(one_session: session):
    """Получение всех бронирований за период от <dfrom> до <dto>"""
    try:
        bookings = one_session.post(
            BASE_URL + '/planning/bookings',
            headers={
                'Accept': 'application/json',
                'X-Requested-With': 'XMLHttpRequest'
            },
            data={
                # "dfrom": "2022-09-10",
                "dfrom": datetime.date.today().strftime('%Y-%m-%d'),
                "dto": "2024-12-31",
                "daily": 0
            }
        )
        result: list[dict] = bookings.json().get('result')
        logging.debug(f'получено броней: {len(result)}шт.')
        return result
    except Exception as e:
        logging.error('Ошибка запроса к bnovo')


def write_to_data_base(all_booking) -> None:
    """Записывает данные в базу из списка словарей all_booking."""
    for item in all_booking:
        if not Customer.objects.filter(booking_id=item["booking_id"]):
            Customer.objects.create(
                booking_id=item.get('booking_id'),
                phone=item.get('phone').replace('\xa0', ''),
                full_name=item.get('customer').title(),
                date=item.get('date'),
                real_arrival=item.get('real_arrival'),
                real_departure=item.get('real_departure'),
                room_id=item.get('room_id'),
                email=item.get('email'),
                source=item.get('source'),
            )


def update_data_base(all_booking):
    try:
        for item in all_booking:
            values_for_update = {
                'phone': item.get('phone', '-').replace('\xa0', ''),
                'full_name': item.get('customer', '').title(),
                'date': item.get('date'),
                'real_arrival': item.get('real_arrival')[:-3],
                'real_departure': item.get('real_departure')[:-3],
                'room_id': item.get('room_id'),
                'adults': item.get('adults'),
                'email': item.get('email', '-'),
                'source': item.get('source'),
            }
            Customer.objects.update_or_create(
                booking_id=item.get('booking_id'),
                defaults=values_for_update
            )
        logging.info('Записано в базу данных')
    except Exception as e:
        logging.error('Не удалось записать в базу данных')


class Command(BaseCommand):
    help = "Запись в базу данных"

    def handle(self, *args, **kwargs):
        try:
            print('Start')
            while True:
                # write_to_data_base(get_all_booking(session))
                update_data_base(get_all_booking(session))
                pprint(get_all_booking(session))
                time.sleep(10)
        except:
            logging.error('handle не отработал.')
            raise CommandError('Сбой')
