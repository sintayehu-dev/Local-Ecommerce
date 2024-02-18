from django.shortcuts import render
from django.http import JsonResponse
import datetime
from .models import *
import json
from .utils import *

def store(request):
    Data=cartData(request)
    cartItems=Data['cartItems']
        
    products=Product.objects.all()
    context = {'products':products, 'cartItems':cartItems}
    return render(request, 'store/store.html', context)

def cart(request):
    
    Data=cartData(request)
    items=Data['items']
    order=Data['order']
    cartItems=Data['cartItems']
        
        
    context = {'items':items, 'order':order, 'cartItems':cartItems}
    return render(request, 'store/cart.html', context)

from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def checkout(request): 
    Data=cartData(request)
    items=Data['items']
    order=Data['order']
    cartItems=Data['cartItems']
    context = {'items':items, 'order':order, 'cartItems':cartItems }
       
    
    return render(request, 'store/checkout.html', context)


def updateItem(request):
    data = json.loads(request.body.decode('utf-8'))
    productId = data.get('productId')
    action = data.get('action')
    print('Product ID:', productId)
    print('Action:', action)

    if not request.user.is_authenticated:
        return JsonResponse({'error': 'User is not authenticated.'}, status=401)

    customer = request.user.customer
    try:
        product = Product.objects.get(id=productId)
    except Product.DoesNotExist:
        return JsonResponse({'error': 'Product does not exist.'}, status=404)

    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity += 1
    elif action == 'remove':
        orderItem.quantity -= 1

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse({'message': 'Item is updated successfully.'}, safe=False)
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def processOrder(request):
    data = json.loads(request.body)
    transaction_id = datetime.datetime.now().timestamp()

    if request.user.is_authenticated:
        customer = request.user.customer
        order = Order.objects.create(customer=customer, complete=False)

    else:
       customer, order=guestOrder(request, data)

    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == order.total_price:
        order.complete = True

    order.save()

    if order.shipping:
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            state=data['shipping']['state'],
            zipcode=data['shipping']['zipcode'],
        )

    return JsonResponse('payment submitted......', safe=False)

    
    