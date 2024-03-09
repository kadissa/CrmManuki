"""
Получает данные клиентов с сайта по API, парсит их и записывает в файл CSV.
"""
import csv
import datetime
import os

import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = 'https://online.bnovo.ru'
LOGIN = os.getenv('BNOVO_API_LOGIN')
PASSWORD = os.getenv('BNOVO_API_PASSWORD')
session = requests.Session()

HEADERS = {
    'username': LOGIN,
    'password': PASSWORD
}
response = session.post(BASE_URL, data=HEADERS)
room_type = session.get(BASE_URL + '/roomTypes/get',
                        headers={'Accept': 'application/json'})
room = session.get(BASE_URL + '/room',
                   headers={'Accept': 'application/json'})
tariff = session.get(BASE_URL + '/tariff/tariffs',
                     headers={'Accept': 'application/json'})
bookings = session.post(BASE_URL + '/planning/bookings',
                        headers={
                            'Accept': 'application/json',
                            'X-Requested-With': 'XMLHttpRequest'
                        },
                        data={
                            "dfrom": "2024-03-04",
                            # "dfrom": datetime.date.today().strftime('%Y-%m-%d'),
                            "dto": "2024-12-31",
                            "daily": 0
                        }
                        )
source_data: list[dict] = bookings.json().get('result')
c = 1

# values = [i.get('phone') for i in end_data]


# for number, dict_ in enumerate(end_data):
#     csv = dict_.get('phone')
#     # print(
#     #     f"{c}Телефон:{dict_.get('phone')}, Имя:{dict_.get('name')},"
#     #     f" Пользователь:{dict_.get('customer')}",
#     #     f"Дата:{dict_.get('date')}, Email:{dict_.get('email')},"
#     #     f" Откуда:{dict_.get('source')}",
#     #     f"Фамилия:{dict_.get('surname')}, "
#     #     f"UUID:{dict_.get('booking_id')}"
#     # )
#     print(number+1,csv)
#     c += 1
booking_ids = [key.get('booking_id') for key in source_data]


def check_booking_id(bookings_id):
    with open('guests.csv', 'r', encoding='utf-8') as file:
        for line in file:
            id_in_baza = line.split(',')[-1].strip()
            if id_in_baza == bookings_id:
                return False
    return True


with open("guests.csv", mode="a+", encoding='utf-8') as w_file:
    file_writer = csv.writer(w_file, delimiter=",", lineterminator="\r")
    # file_writer.writerow(
    #     ["Телефон", "Имя", "Пользователь", "Дата", "Email", "Откуда",
    #      "Фамилия", "UUID_bnovo"]
    # )
    for dict_ in source_data:
        booking_id = dict_.get('booking_id')
        if check_booking_id(booking_id):
            file_writer.writerow(
                [dict_.get('phone').replace('\xa0', ''),
                 dict_.get('name'),
                 dict_.get('customer'),
                 dict_.get('date'),
                 dict_.get('email'),
                 dict_.get('source'),
                 dict_.get('surname'),
                 dict_.get('booking_id')]
            )
