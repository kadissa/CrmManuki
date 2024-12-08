import datetime
import os
import time
import logging
import requests
from django.core.management.base import BaseCommand, CommandError
from bnovo.models import Customer

logging.basicConfig(
    level=logging.DEBUG,
    filename="logs/bnovo_parser.log",
    filemode="a",
    format="%(asctime)s, %(levelname)s, " "%(message)s, %(name)s, %(funcName)s",
)
BASE_URL = "https://online.bnovo.ru"
LOGIN = os.getenv("BNOVO_API_LOGIN")
PASSWORD = os.getenv("BNOVO_API_PASSWORD")
session = requests.Session()

HEADERS = {"username": LOGIN, "password": PASSWORD}

response = session.post(BASE_URL, data=HEADERS)


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
            BASE_URL + "/planning/bookings",
            headers={
                "Accept": "application/json",
                "X-Requested-With": "XMLHttpRequest",
            },
            data={
                # "dfrom": "2022-09-10",
                "dfrom": datetime.date.today().strftime("%Y-%m-%d"),
                "dto": "2024-12-31",
                "daily": 0,
            },
        )
        result: list[dict] = bookings.json().get("result")
        logging.debug(f"получено броней: {len(result)}шт.")
        return result
    except Exception as e:
        logging.error("Ошибка запроса к bnovo", e)


def write_to_data_base(all_booking) -> None:
    """Записывает данные в базу из списка словарей all_booking."""
    for item in all_booking:
        if not Customer.objects.filter(booking_id=item["booking_id"]):
            Customer.objects.create(
                booking_id=item.get("booking_id"),
                phone=item.get("phone").replace("\xa0", ""),
                full_name=item.get("customer").title(),
                date=item.get("date"),
                real_arrival=item.get("real_arrival"),
                real_departure=item.get("real_departure"),
                room_id=item.get("room_id"),
                email=item.get("email"),
                source=item.get("source"),
            )


def update_data_base(all_booking):
    """
    Updates the database with the given list of booking dictionaries.
    For each booking, it looks up the corresponding record in the database
    and updates the fields with the values from the dictionary.
    If the record doesn't exist, it creates a new one.
    """
    try:
        # print("update_database started")  # for debugging
        for item in all_booking:
            # Create a dictionary with the values to update
            values_for_update = {
                "phone": item.get("phone", "-").replace("\xa0", ""),
                "full_name": item.get("customer", "").title(),
                "date": item.get("date"),
                "real_arrival": item.get("real_arrival")[:-3],
                "real_departure": item.get("real_departure")[:-3],
                "room_id": item.get("room_id"),
                "adults": item.get("adults"),
                "email": item.get("email", "-"),
                "source": item.get("source"),
            }
            # Update or create the record in the database
            Customer.objects.update_or_create(
                booking_id=item.get("booking_id"), defaults=values_for_update
            )
        logging.info("Записано в базу данных")
    except Exception as e:
        logging.error("Не удалось записать в базу данных", e)


class Command(BaseCommand):
    help = "Запись в базу данных"

    def handle(self, *args, **kwargs):
        """
        This is the main loop of the script. It runs indefinitely and
        every 10 seconds it fetches the data from bnovo and writes it
        to the database.
        """
        try:
            while True:
                # write_to_data_base(get_all_booking(session))
                # Update the database with the new data
                update_data_base(get_all_booking(session))
                # wait 10 seconds before the next iteration
                time.sleep(10)
        except Exception as e:
            # Log the error
            logging.error("handle не отработал.", e)
            # Raise a Django CommandError
            raise CommandError("Сбой")
