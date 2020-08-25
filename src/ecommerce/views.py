from django.contrib.auth import authenticate, login, get_user_model
from django.shortcuts import render, redirect

from .forms import ContactForm


def home_page(request):
    # print(request.session.get('first_name', 'Unknown'))
    context = {
        "title": "hello world!",
        "content": "welcome to the home page",
    }
    if request.user.is_authenticated():
        context['premium_content'] = "amazing"
    return render(request, 'home_page.html', context)


def about_page(request):
    context = {
        "title": "about world!",
        "content": "welcome to the about page",
    }
    return render(request, 'home_page.html', context)


def contact_page(request):
    contact_form = ContactForm(request.POST or None)
    context = {
        "title": "contact world!",
        "content": "welcome to the contact page",
        'form': contact_form,
        "brand": "New Brand Name"
    }

    if contact_form.is_valid():
        print(contact_form.cleaned_data)

    return render(request, 'contact/view.html', context)
