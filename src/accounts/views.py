from django.views.generic import CreateView, FormView
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.views.generic import CreateView, FormView, DetailView, View
from django.shortcuts import render, redirect
from django.utils.http import is_safe_url
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe

from .forms import LoginForm, RegisterForm, GuestForm
from .models import GuestEmail, EmailActivation
from .signals import user_logged_in


# @login_required
# def account_home_view(request):
#     return render(request, "accounts/home.html")


class AccountHomeView(LoginRequiredMixin, DetailView):
    template_name = 'accounts/home.html'

    def get_object(self):
        return self.request.user


class AccountEmailActivateView(View):
    def get(self, request, key, *args, **kwargs):
        qs = EmailActivation.objects.filter(key__iexact=key)
        confirm_qs = qs.confirmable()
        if confirm_qs.count() == 1:
            obj = confirm_qs.first()
            obj.activate()
            messages.success(
                request, "Your email has been confirmed. Please login.")
            return redirect("login")
        else:
            activated_qs = qs.filter(activated=True)
            if activated_qs.exists():
                reset_link = reverse("password_reset")
                msg = """Your email has already been confirmed
                Do you need to <a href="{link}">reset your password</a>?
                """.format(link=reset_link)
                messages.success(request, mark_safe(msg))
                return redirect("login")
        return render(request, 'registration/activation-error.html', {})

    def post(self, request, *args, **kwargs):
        pass


class LoginView(FormView):
    form_class = LoginForm
    success_url = '/'
    template_name = 'accounts/login.html'

    def form_valid(self, form):
        request = self.request
        next_ = request.GET.get('next')
        next_post = request.POST.get('next')
        redirect_path = next_ or next_post or None

        email = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(request, username=email, password=password)
        if user is not None:
            if not user.is_active:
                messages.error(request, "This user is inactive")
                return super(LoginView, self).form_invalid(form)
            login(request, user)
            user_logged_in.send(user.__class__, instance=user, request=request)
            try:
                del request.session['guest_email_id']
            except:
                pass
            if is_safe_url(redirect_path, request.get_host()):
                return redirect(redirect_path)
            else:
                return redirect("/")
        return super(LoginView, self).form_invalid(form)


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'accounts/register.html'
    success_url = '/login'


def guest_register_view(request):
    form = GuestForm(request.POST or None)
    context = {
        "form": form
    }
    next_ = request.GET.get('next')
    next_post = request.POST.get('next')
    redirect_path = next_ or next_post or None
    if form.is_valid():
        email = form.cleaned_data.get("email")
        new_guest_email = GuestEmail.objects.create(email=email)
        request.session['guest_email_id'] = new_guest_email.id
        if is_safe_url(redirect_path, request.get_host()):
            return redirect(redirect_path)
        else:
            return redirect("/register/")
    return redirect("/register/")
