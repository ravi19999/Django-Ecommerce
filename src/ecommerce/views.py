from django.shortcuts import render
from django.http import HttpResponse

from .forms import ContactForm


def home_page(request):
    context = {
        "title": "hello world!",
        "content": "welcome to the home page"
    }
    return render(request, 'home_page.html', context)


def about_page(request):
    context = {
        "title": "about world!",
        "content": "welcome to the about page"

    }
    return render(request, 'home_page.html', context)


def contact_page(request):
    contact_form = ContactForm(request.POST or None)
    context = {
        "title": "contact world!",
        "content": "welcome to the contact page",
        'form': contact_form
    }

    if contact_form.is_valid():
        print(contact_form.cleaned_data)
    # if request.method == 'POST':
    #     print(request.POST.get('fullname'))
    #     print(request.POST.get('email'))
    #     print(request.POST.get('content'))
    return render(request, 'contact/view.html', context)
