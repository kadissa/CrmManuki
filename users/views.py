import time

from django.contrib.auth import logout
from django.shortcuts import redirect, get_object_or_404, render
from django.views.generic import UpdateView
# from .forms import GuestSelfEditForm
# from webhooks.models import Guest, Item
from django.core.mail import send_mail
import threading

import os


def logout_view(request):
    logout(request)
    return redirect('login')


# def guest_self_edit(request, booking_id, sauna_price):
#     # time.sleep(2)
#     if not Guest.objects.filter(
#             booking_id=booking_id, price=sauna_price).order_by('id').last():
#         return redirect('https://manuki.easyweek.ru')
#     guest = Guest.objects.filter(
#         booking_id=booking_id, price=sauna_price).order_by('id').last()
#     if guest.status == 'Отменено':
#         return redirect('https://manuki.easyweek.ru')
#     form = GuestSelfEditForm(request.POST or None, instance=guest)
#     cost_per_hour = int(int(guest.price[:-2]) / int(guest.duration[0]))
#     form.set_label_rotenburo(cost_per_hour)
#     if form.is_valid():
#         form.save(commit=False)
#         rotenburo_price = (guest.rotenburo_1 or 0) * cost_per_hour
#         oak_broom_price = (guest.oak_broom or 0) * 300
#         birch_broom_price = (guest.birch_broom or 0) * 300
#         bed_sheet_price = (guest.bed_sheet or 0) * 100
#         towel_price = (guest.towel or 0) * 100
#         robe_price = (guest.robe or 0) * 100
#         slippers_price = (guest.slippers or 0) * 100
#         total_accessories_price = sum(
#             [oak_broom_price, birch_broom_price, bed_sheet_price,
#              towel_price, robe_price, slippers_price, rotenburo_price]
#         )
#         sauna_price = int(guest.price[:-2])
#         total_price = total_accessories_price + sauna_price
#         item = Item.objects.update_or_create(
#             defaults={
#                 'base_sauna_price': sauna_price,
#                 'guest_id': guest,
#                 'rotenburo': rotenburo_price,
#                 'oak_broom': oak_broom_price,
#                 'birch_broom': birch_broom_price,
#                 'bed_sheet': bed_sheet_price,
#                 'towel': towel_price,
#                 'robe': robe_price,
#                 'slippers': slippers_price},
#             guest_id_id=guest.id
#         )
#         guest.price_formatted = total_price
#         guest.price = total_price * 100
#         guest.save(update_fields=['price_formatted', 'price'])
#         form.save()
#         threading.Thread(target=client_mail, args=(guest, item[0])).start()
#         return redirect('users:success_url', pk=guest.id)
#     return render(request, 'guest_self_edit.html',
#                   context={'object': guest, 'form': form})



def extend_services_mail(guest, items):
    rotenburo_count = guest.rotenburo_1 or 0
    oak_broom_count = guest.oak_broom or 0
    birch_broom_count = guest.birch_broom or 0
    bed_sheet_count = guest.bed_sheet or 0
    towel_count = guest.towel or 0
    robe_count = guest.robe or 0
    slippers_count = guest.slippers or 0
    message = (f'Ротенбуро - {rotenburo_count} ч. {items.rotenburo}руб.\n'
               f'Веник берёза - {birch_broom_count}шт.- '
               f'{items.birch_broom}руб.\nВеник дуб -'
               f'{oak_broom_count}шт.- {items.oak_broom}руб.\nПростыня - '
               f'{bed_sheet_count}шт. - {items.bed_sheet}руб.\nПолотенце - '
               f'{towel_count}шт.- {items.towel}р.\nХалат - {robe_count}шт. '
               f'- {items.robe}руб.\nТапки - {slippers_count}шт.- '
               f'{items.slippers}руб.\nна сумму '
               f'{items.total_accessories_price}.\nОбщая сумма '
               f'{items.total_price}\nВремя посещения: {guest.start[:-6]} '
               f' с {guest.start[-6:]}, до {guest.end[-6:]}')
    return message


def client_mail(guest, items):
    mail = send_mail(
        subject='Бронирование бани',
        message=f'{guest.ful_name}, вы заказали доп. услуги: \n' +
                extend_services_mail(guest, items),
        from_email=os.getenv('EMAIL_HOST_USER'),
        recipient_list=[
            f'{guest.email}',
            'manuki.en178@gmail.com'
        ]
    )
    return mail


# def get_success(request, pk):
#     guest = get_object_or_404(Guest, id=pk)
#     items = get_object_or_404(Item, guest_id=guest)
#     context = {'object': items, 'guest': guest}
#     # threading.Thread(target=client_mail, args=(guest, items)).start()
#     return render(request, 'success.html', context)
