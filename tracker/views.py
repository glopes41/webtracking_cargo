from django.urls import reverse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.http import JsonResponse
import json
from django.core.cache import cache
from django.utils.timezone import now
from django.middleware.csrf import get_token
from order_manager.models import Order
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import threading


location = {}
loc = {}
orders = {}
lock = threading.Lock()


def get_csrf_token(request):
    return JsonResponse({'csrftoken': get_token(request)})


# Motorista escolhe a entrega e envia para o sistema
@login_required(login_url='driver:login', redirect_field_name='next')
def delivery_choice(request):
    if request.method == 'POST':
        id_order = request.POST.get('id')
        id_driver = request.user.id
        print("request:", id_driver)

        if (id_order != None) and (id_driver != None):
            try:
                order = Order.objects.get(id=id_order)
            except Order.DoesNotExist:
                return JsonResponse({"message": "Ordem não encontrada!"}, status=404)

            try:
                driver = User.objects.get(id=id_driver)
            except User.DoesNotExist:
                return JsonResponse({"message": "Motorista não cadastrado!"}, status=404)

            order.status = "transito"
            order.driver = driver

            try:
                order.full_clean()
            except ValidationError as error:
                print(error.messages)
                return JsonResponse({"message": "Erro interno"}, status=500)

            order.save()

            return redirect('tracker:tracking')

    elif request.method == 'GET':
        orders = Order.objects.filter(status='pendente')

        return render(request, 'tracker/pages/deliveries_available.html', context={'orders': orders, "timestamp": now().timestamp()})


@login_required(login_url='driver:login', redirect_field_name='next')
def tracking_driver(request):
    return render(request, 'tracker/pages/tracking_driver.html', {"timestamp": now().timestamp()})


@login_required(login_url='driver:login', redirect_field_name='next')
def update_location(request):
    '''Receive a new location from client tracked'''
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            latitude = float(data.get('latitude'))
            longitude = float(data.get('longitude'))

            if latitude is None or longitude is None:
                return JsonResponse({'error': 'Latitude e longitude são obrigatórias'}, status=400)

            driver_id = request.user.id
            order_id = request.session.get("order_in_progress")
            try:
                driver = User.objects.get(id=driver_id)
                driver_name = driver.get_full_name()
            except User.DoesNotExist:
                driver_name = "Desconhecido"

            if not order_id:
                return JsonResponse({'error': 'Ordem em andamento não encontrada na sessão'}, status=400)

            tracking_data = {
                'order_id': order_id['order_id'],
                'driver_name': driver_name,
                'latitude': latitude,
                'longitude': longitude,
                'timestamp': now().isoformat()
            }

            cache_key = f"order_{order_id['order_id']}"
            cache.set(cache_key, tracking_data, timeout=3600)
            print("🔑 Salvando em cache:", cache_key)

            global location
            order_id = request.session.get("order_in_progress")
            location = {'lat': latitude, 'lon': longitude}
            print(f'📍 Nova posição: {latitude}, {longitude}')
            return JsonResponse({'status': 'OK', 'location': location, 'order_id': order_id})

        except json.JSONDecodeError:
            return JsonResponse({'error': 'JSON inválido'}, status=400)

    else:
        return JsonResponse({'error': 'Método não permitido'}, status=405)


@login_required(login_url='driver:login', redirect_field_name='next')
def show_map(request, order_id):
    '''Show map with route'''

    return render(request, 'tracker/pages/map.html', {'route': location, 'timestamp': now().timestamp()})


@login_required(login_url='driver:login', redirect_field_name='next')
def get_route(request, order_id):
    '''Return routes coordinates'''
    print("order:", order_id)
    cache_key = f"order_{order_id}"
    location = cache.get(cache_key)
    print("📍 Dados recuperados:", location)
    return JsonResponse({'locations': location})
