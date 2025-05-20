from django.shortcuts import render, redirect
from django.utils.timezone import now
from django.contrib import messages
from django.core.exceptions import ValidationError
from order_manager.models import Order, Client
from .forms import OrderForm
from django.contrib.auth.models import User
from django.http import JsonResponse
import json
from django.http import Http404
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

# Testada


@login_required(login_url='driver:login', redirect_field_name='next')
def order_list(request):
    orders = Order.objects.all()
    print(orders)
    return render(request, 'order_manager/pages/orders.html',
                  context={'orders': orders, "timestamp": now().timestamp()})

# Testada


@login_required(login_url='driver:login', redirect_field_name='next')
def order_register(request):
    register_form_data = request.session.get('form_data', None)
    # form = OrderForm(register_form_data) if register_form_data else OrderForm()
    if register_form_data:
        form = OrderForm(register_form_data)
    else:
        form = OrderForm()

    return render(request, 'order_manager/pages/orders_register.html', context={'form': form, "timestamp": now().timestamp()})

# Testada


@login_required(login_url='driver:login', redirect_field_name='next')
def register_verify(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Ordem cadastrada com sucesso!")
            if 'form_data' in request.session:
                del request.session['form_data']
            return redirect('order_manager:register')

        request.session['form_data'] = request.POST
        messages.error(request, "Erro ao cadastrar ordem. Verifique os dados.")
        return redirect('order_manager:register')
    raise Http404("Método não permitido.")

# Testada
# choice.js chama essa view para pegar lista de ordens abertas!


@login_required(login_url='driver:login', redirect_field_name='next')
def order_open_list(request):
    orders = Order.objects.filter(status='pendente')
    orders_json = list(orders.values(
        'id', 'client__name', 'delivery_date', 'status'))

    return JsonResponse(orders_json, safe=False)


@login_required(login_url='driver:login', redirect_field_name='next')
def order_status_update(request):
    """Update order status"""
    if request.method != "POST":
        return JsonResponse({"message": "Método GET não permitido."}, status=405)

    try:
        data = json.loads(request.body)
        id_status = data.get("status")
        if not id_status:
            return JsonResponse({"message": "Status do pedido não fornecido."}, status=400)

        id_order = data.get("id_order")
        if not id_order:
            return JsonResponse({"message": "ID do pedido não fornecido."}, status=400)

        # id_driver = data.get("id_driver")
        # if not id_driver:
        #     return JsonResponse({"message": "ID do motorista não fornecido."}, status=400)

        status_list = [status[0] for status in Order.STATUS_CHOICES]
        if id_status not in status_list:
            return JsonResponse({"message": "Status fornecido inválido"}, status=400)

        try:
            order = Order.objects.get(id=id_order)
        except Order.DoesNotExist:
            return JsonResponse({"message": "Orderm não encontrada."}, status=404)

        try:
            id_driver = request.user.id
            driver = User.objects.get(id=id_driver)
        except User.DoesNotExist:
            return JsonResponse({"message": "Motorista não cadastrado."}, status=404)

        # order.driver = driver
        order.status = id_status
        order.save()
        if 'order_in_progress' in request.session:
            del request.session["order_in_progress"]

        return JsonResponse({"message": "Status da entrega alterado",
                             "order": {"id": order.pk, "status": order.status, "driver": driver.first_name}}, status=200)

    except json.JSONDecodeError:
        return JsonResponse({"message": "Erro ao processar JSON."}, status=400)


@login_required(login_url='driver:login', redirect_field_name='next')
def order_choiced(request):
    if request.method != 'POST':
        return JsonResponse({"message": "Método GET não permitido."}, status=405)

    try:
        data = json.loads(request.body)

        id_order = data.get("id_order")
        if not id_order:
            return JsonResponse({"message": "ID do pedido não fornecido."}, status=400)

        # id_driver = request.user.id
        # if not id_driver:
        #     return JsonResponse({"message": "ID do motorista não fornecido."}, status=400)

        try:
            order = Order.objects.get(id=id_order)
        except Order.DoesNotExist:
            return JsonResponse({"message": "Ordem não encontrada!"}, status=404)

        try:
            id_driver = request.user.id
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
        request.session['order_in_progress'] = {
            'order_id': order.pk, 'driver_id': driver.pk}
        return JsonResponse({"message": "OK",
                            "order": {"id": order.pk, "status": order.get_status_display(), "driver": driver.first_name}}, status=200)

    except json.JSONDecodeError:
        return JsonResponse({"message": "Erro ao processar JSON."}, status=400)


@login_required(login_url='driver:login', redirect_field_name='next')
def order_in_progress(request):
    order = request.session.get("order_in_progress")
    print(order)
    if order is None:
        return JsonResponse({})
    else:
        return JsonResponse({'order': order})


@login_required(login_url='driver:login', redirect_field_name='next')
def order_search(request):
    User = get_user_model()

    status = request.GET.get("status")
    client_id = request.GET.get("client")
    driver_id = request.GET.get("driver")

    ordens = Order.objects.select_related("client", "driver").all()
    clientes = Client.objects.all()
    print(clientes)
    motoristas = User.objects.filter(order__isnull=False).distinct()

    if status:
        ordens = ordens.filter(status=status)
    if client_id:
        ordens = ordens.filter(client__id=client_id)
    if driver_id:
        ordens = ordens.filter(driver__id=driver_id)

    return render(request, "order_manager/pages/search.html", {
        "ordens": ordens,
        "clientes": clientes,
        "motoristas": motoristas,
        "status_selecionado": status,
        "client_selecionado": client_id,
        "driver_selecionado": driver_id,
        "timestamp": now().timestamp(),
    })
