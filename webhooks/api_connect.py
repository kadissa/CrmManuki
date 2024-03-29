"""
Получает и отправляет данные по API.
"""
import datetime
import logging
import os
import time

import requests
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.DEBUG, filename='logs/api_connect.log',
                    filemode='a', format='%(asctime)s, %(levelname)s, '
                                         '%(message)s, %(name)s, %(funcName)s')
BASE_URL = 'https://my.easyweek.io/api/public/v2/'
TOKEN = os.getenv('EASYWEEK_API_TOKEN')
WORKSPACE = os.getenv('WORKSPACE')
LOCATIONS_UUID = os.getenv('LOCATIONS_UUID')
SERVICE_UUID = os.getenv('SERVICE_UUID')
ACCOUNT_UUID = os.getenv('ACCOUNT_UUID')
session = requests.Session()

HEADERS = {
    'Authorization': f'Bearer {TOKEN}',
    'Workspace': 'manuki'
}


def get_free_slots(one_session):
    """Получает слоты, свободные для бронирования."""
    time_slots = one_session.get(
        BASE_URL + 'locations/' + LOCATIONS_UUID +
        f'/time-slots/?service_uuid={SERVICE_UUID}' +
        '&range_start=2024-03-04&range_end=2024-03-05',
        headers=HEADERS)  # Максимальный диапазон 3 месяца
    return time_slots


def cancel_booking(one_session, uuid):
    """Изменяет статус бронирования"""
    time.sleep(3)
    update = one_session.put(
        f'{BASE_URL}bookings/{uuid}/status/cancel',
        headers=HEADERS,
        data={
            "cancel_reason": "wrong_order",
            "internal_notes": ""
        }
    )
    logging.info(f'{update.status_code}')
    logging.info('Уборщик, статус изменён.')
    print(update.status_code)
    return update


def create_booking(one_session, booking_data=None):
    """
    Совершает техническую бронь на один час для уборки после того как
    клиент сделает заказ.
    """
    time.sleep(2)
    date_end = datetime.datetime.fromisoformat(
        booking_data.get('booking_date_end'))
    # logging.debug(date_end.isoformat()[:-6] + 'Z')
    send_booking = one_session.post(
        BASE_URL + 'bookings', headers=HEADERS,
        data={
            "reserved_on": date_end.isoformat()[:-6] + 'Z',
            "location_uuid": LOCATIONS_UUID,
            "service_uuid": SERVICE_UUID,
            "customer_phone": "+79118085565",
            "customer_first_name": "Уборщик",
            "customer_email": "cleaning@clean.com",
            "booking_comment": "Уборка",
            "source": "cleaning",
            "timezone": "Europe/Moscow",
            "customer_browser_tz": "Europe/Moscow",
            "duration": {"value": 60,
                         "label": "minutes",
                         "iso_8601": "PT60M"}
        }

    )
    logging.info(send_booking.status_code)
    return send_booking


if __name__ == '__main__':
    # pprint(get_free_slots(session).json())
    # pprint(create_booking(session))
    cancel_booking(session, '808e14cf-b8d5-4047-ae7e-acf03e9d05f7')
