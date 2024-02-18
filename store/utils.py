import json
from .models import *

def cookieCart(request):
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}

    print('cart', cart)
    items = []
    order = {'total_item': 0, 'total_price': 0, 'shipping': False}  # Initialize 'shipping' to False

    cartItems = order['total_item']

    for i in cart:
        try:
            cartItems += cart[i]['quantity']
            product = Product.objects.get(id=i)
            total = (product.price * cart[i]['quantity'])

            order['total_item'] += cart[i]['quantity']
            order['total_price'] += total
            

            item = {
                'product': {
                    'id': product.id,
                    'name': product.name,
                    'price': product.price,
                    'imageURL': product.imageURL,
                },
                'quantity': cart[i]['quantity'],
                'get_total': total
            }
            items.append(item)
            if not product.digital:
                order['shipping'] = True
        except:
            pass

    return {'cartItems': cartItems, 'order': order, 'items': items}

def cartData(request):
     if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems=order.total_item
     else:
        cookieData= cookieCart(request)
        items=cookieData['items']
        order=cookieData['order']
        cartItems=cookieData['cartItems']
     return{'cartItems': cartItems, 'order': order, 'items': items}


def guestOrder(request, data):
    print('user is not logged in... ')
    print('COOKIES', request.COOKIES)

    name = data['form']['name']
    email = data['form']['email']

    cookieData = cookieCart(request)
    items = cookieData['items']

    customer, created = Customer.objects.get_or_create(email=email)
    customer.name = name
    customer.save()

    order = Order.objects.create(customer=customer, complete=False)

    for item in items:
        product = Product.objects.get(id=item['product']['id'])

        orderItem = OrderItem.objects.create(
            product=product,
            order=order,
            quantity=item['quantity']
        )
    return customer, order