from django.contrib.auth import authenticate, login, get_user_model
from django.shortcuts import render, redirect
from django.http import HttpResponse

from .forms import ContactForm, LoginForm, RegisterForm


def home_page(request):
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


def login_page(request):
    form = LoginForm(request.POST or None)
    context = {
        'form': form
    }
    print(request.user.is_authenticated())
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        print(form.cleaned_data)
        user = authenticate(request, username=username, password=password)
        print(request.user.is_authenticated())
        if user is not None:
            print(request.user.is_authenticated())
            login(request, user)
            context['form'] = LoginForm()
            return redirect('/')
        else:
            print('Error')
    return render(request, 'auth/login.html', context)


User = get_user_model()


def register_page(request):
    form = RegisterForm(request.POST or None)
    context = {
        "form": form
    }
    if form.is_valid():
        print(form.cleaned_data)
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        email = form.cleaned_data.get('email')
        new_user = User.objects.create_user(username, email, password)
        print(new_user)
    return render(request, 'auth/register.html', context)
