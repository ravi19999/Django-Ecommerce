from .models import BillingProfile
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.utils.http import is_safe_url


import stripe
stripe.api_key = "sk_test_51HQwJDE9dKyATRmBfqOTCDB0lrrbYsQ402TLCd9iKBXkmrB4O7Ct3nVkjxK9HiW5Ren13woNiRCnx9lft3HX9Zr000oke1IFQH"
STRIPE_PUB_KEY = 'pk_test_51HQwJDE9dKyATRmBYJ8cUGFJpGeL7pOdz17Pla6gVZEXRLVmjQCTaBSIuL8j96Qv8SYPwVNbuPpSPR9paqcqiUbt00LdZ9DqcB'


def payment_method_view(request):
    # next_url =
    # if request.user.is_authenticated():
    #     billing_profile = request.user.billingprofile
    #     my_customer_id = billing_profile.customer_id

    billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(
        request)
    if not billing_profile:
        return redirect("/cart")
    next_url = None
    next_ = request.GET.get('next')
    if is_safe_url(next_, request.get_host()):
        next_url = next_
    return render(request, 'billing/payment-method.html', {"publish_key": STRIPE_PUB_KEY, "next_url": next_url})


def payment_method_create_view(request):
    if request.method == "POST" and request.is_ajax():
        billing_profile = BillingProfile.objects.new_or_get(request)
        if not billing_profile:
            return HttpResponse({"message": "Cannot find this user"}, status_code=401)
        token = request.POST.get("stripeToken")
        if token is not None:
            customer = stripe.Customer.retrieve(billing_profile.customer_id)
            card_response = customer.sources.create(source=token)
            print(card_response)  # start saving our cards too!
        return JsonResponse({"message": "Success! Your card was added."})
    return HttpResponse("error", status_code=401)
