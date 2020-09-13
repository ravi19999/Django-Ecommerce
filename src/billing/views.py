from django.shortcuts import render

import stripe
stripe.api_key = 'sk_test_51HQwJDE9dKyATRmBfqOTCDB0lrrbYsQ402TLCd9iKBXkmrB4O7Ct3nVkjxK9HiW5Ren13woNiRCnx9lft3HX9Zr000oke1IFQH'
STRIPE_PUB_KEY = 'pk_test_51HQwJDE9dKyATRmBYJ8cUGFJpGeL7pOdz17Pla6gVZEXRLVmjQCTaBSIuL8j96Qv8SYPwVNbuPpSPR9paqcqiUbt00LdZ9DqcB'


def payment_method_view(request):
    if request.method == "POST":
        print(request.POST)
    return render(request, 'billing/payment-method.html', {"publish_key": STRIPE_PUB_KEY})
