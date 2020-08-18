from django.shortcuts import render

# Create your views here.


def cart_home(request):
    cart_id = request.session.get('cart_id', None)
    if cart_id is None:
        print('create new cart')
        request.session['cart_id'] = 12
    else:
        print('Cart ID exists')

    return render(request, "carts/home.html", {})
