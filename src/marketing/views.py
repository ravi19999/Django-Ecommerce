from django.shortcuts import render
from django.views.generic import UpdateView

from .forms import MarketingPreferenceFrom
from .models import MarketingPreference


class MarketingPreferenceUpdateView(UpdateView):
    form_class = MarketingPreferenceFrom
    template_name = 'base/forms.html'
    success_url = '/settings/email'

    def get_context_data(self, *args, **kwargs):
        context = super(MarketingPreferenceUpdateView,
                        self).get_context_data(*args, **kwargs)
        context['title'] = "Update Email Preferences"
        return context

    def get_object(self):
        user = self.request.user
        obj, created = MarketingPreference.objects.get_or_create(user=user)
        return obj
