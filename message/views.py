from datetime import date
from django.shortcuts import render
from django.views import generic
from . import models
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
class Message_Create(LoginRequiredMixin, generic.CreateView):
    model = models.Message
    fields = ['text', 'to_user']
    template_name = 'message/create.html'

    def form_valid(self,form):
        self.object = form.save(commit=False)
        self.object.from_user = self.request.user
        self.object.save()
        return super().form_valid(form)

class Message_user_view(LoginRequiredMixin, generic.TemplateView):
    template_name = 'message/message_view.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["message_from"] = models.Message.objects.filter(to_user=self.request.user, from_user=self.kwargs.get('pk')).order_by('-send_of')
        context["message_to"] = models.Message.objects.filter(from_user=self.request.user, to_user=self.kwargs.get('pk')).order_by('-send_of')
        return context