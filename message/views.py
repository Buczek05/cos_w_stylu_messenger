from datetime import date
from django import template
from django.shortcuts import render
from django.views import generic
from . import models, forms
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.utils.timezone import now, timedelta, datetime
from django.conf import settings

User = get_user_model()
# Create your views here.

def to_user_make(self):
    if self.kwargs.get('pk'):
        return User.objects.get(pk=self.kwargs.get('pk'))
    else:
        try:
            if models.Message.objects.filter(Q(to_user=self.request.user) | Q(from_user=self.request.user)).latest('send_of').to_user != self.request.user:
                return models.Message.objects.filter(Q(to_user=self.request.user) | Q(
                    from_user=self.request.user)).latest('send_of').to_user
            else:
                return models.Message.objects.filter(Q(to_user=self.request.user) | Q(
                    from_user=self.request.user)).latest('send_of').from_user

        except:
            return 0


class index(generic.TemplateView):
    template_name = 'message/index.html'

class Create_message_js(LoginRequiredMixin, generic.CreateView):
    form_class = forms.Message_form
    template_name = 'message/js_create.html'

    def form_valid(self, form):
        to_user = to_user_make(self)
        self.object = form.save(commit=False)
        self.object.to_user = to_user
        self.object.from_user = self.request.user
        return super().form_valid(form)

class check_message_js(LoginRequiredMixin, generic.TemplateView):
    template_name = 'message/js_check.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        to_user = to_user_make(self)
        if to_user:
            context['message'] = models.Message.objects.filter(
                Q(to_user=self.request.user, from_user=to_user) |
                Q(from_user=self.request.user, to_user=to_user), send_of__range=(now() - timedelta(seconds=10), now())
            ).order_by('pk')
        return context
class previous_add_js(LoginRequiredMixin, generic.TemplateView):
    template_name = 'message/js_check.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        to_user = to_user_make(self)
        if to_user:
            context['message'] = models.Message.objects.filter(
                Q(to_user=self.request.user, from_user=to_user) |
                Q(from_user=self.request.user, to_user=to_user), pk__lt=self.kwargs.get('last')
            ).order_by('pk')[::-1]
            many_massege = len(context['message'])
            if many_massege >= 30:
                context['message'] = context['message'][0:30]

        return context

class Message_user_view(LoginRequiredMixin, generic.CreateView):
    template_name = 'message/message_view.html'
    form_class = forms.Message_form
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users'] = User.objects.exclude(username=self.request.user.username)
        to_user = to_user_make(self)
        if to_user:
            webpush_settings = getattr(settings, 'WEBPUSH_SETTINGS', {})
            vapid_key = webpush_settings.get('VAPID_PUBLIC_KEY')
            context['vapid_key'] = vapid_key
            message_list = models.Message.objects.filter(
                Q(to_user=self.request.user, from_user=to_user) |
                Q(from_user=self.request.user, to_user=to_user)
            ).order_by('-pk')[0:30]
            context["message"] = message_list[::-1]
            context['to_user'] = to_user
        return context

    def form_valid(self, form):
        to_user = to_user_make(self)
        self.object = form.save(commit=False)
        self.object.to_user = to_user
        self.object.from_user = self.request.user
        return super().form_valid(form)
