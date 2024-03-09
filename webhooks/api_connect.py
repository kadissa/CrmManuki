"""
Получает и отправляет данные по API.
"""
import os
import time
from pprint import pprint

import requests
from dotenv import load_dotenv

load_dotenv()

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


def create_booking(one_session, booking_data=None):
    """
    Совершает техническую бронь на один час для уборки после того как
    клиент сделает заказ.
    """
    time.sleep(3)
    send_booking = one_session.post(
        BASE_URL + 'bookings', headers=HEADERS,
        data={
            "reserved_on": booking_data.get('booking_date_end')[:-5] + 'Z',
            "location_uuid": LOCATIONS_UUID,
            "service_uuid": SERVICE_UUID,
            "customer_phone": "+70000000000",
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

    return send_booking


if __name__ == '__main__':
    # pprint(get_free_slots(session).json())
    pprint(create_booking(session))
