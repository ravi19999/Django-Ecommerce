from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.utils.http import is_safe_url

import stripe


stripe.api_key = 'sk_test_51HQwJDE9dKyATRmBfqOTCDB0lrrbYsQ402TLCd9iKBXkmrB4O7Ct3nVkjxK9HiW5Ren13woNiRCnx9lft3HX9Zr000oke1IFQH'
STRIPE_PUB_KEY = 'pk_test_51HQwJDE9dKyATRmBYJ8cUGFJpGeL7pOdz17Pla6gVZEXRLVmjQCTaBSIuL8j96Qv8SYPwVNbuPpSPR9paqcqiUbt00LdZ9DqcB'


def payment_method_view(request):
    next_url = None
    next_ = request.GET.get('next')
    if is_safe_url(next_, request.get_host()):
        next_url = next_
    return render(request, 'billing/payment-method.html', {"publish_key": STRIPE_PUB_KEY, 'next_url': next_url})


def payment_method_create_view(request):
    if request.method == "POST":
        print(request.POST)
        return JsonResponse({"message": 'Done'})
    return HttpResponse("error", status_code=401)
