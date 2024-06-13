from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import DeleteView, DetailView, ListView, UpdateView, CreateView, TemplateView

from mailing.models import MailingSettings, MailingMessage, MailingStatus


class HomeTemplateView(TemplateView):
    """Контроллер для главной страницы"""
    template_name = 'mailing/home.html'


class MailingMessageCreateView(CreateView):
    model = MailingMessage
    fields = ['title', 'content']
    success_url = reverse_lazy('mailing:list')


class MailingMessageUpdateView(UpdateView):
    model = MailingMessage
    fields = ['title', 'content']
    success_url = reverse_lazy('mailing:list')


class MailingMessageDeleteView(DeleteView):
    model = MailingMessage
    success_url = reverse_lazy('mailing:list')


class MailingMessageListView(ListView):
    model = MailingMessage


class MailingMessageDetailView(DetailView):
    model = MailingMessage


class MailingSettingsCreateView(CreateView):
    model = MailingSettings
    fields = ['sending', 'clients', 'message', 'end_time']
    success_url = reverse_lazy('mailing:settings_list')


class MailingSettingsUpdateView(UpdateView):
    model = MailingSettings
    fields = ['sending', 'clients', 'message', 'end_time']
    success_url = reverse_lazy('mailing:settings_list')


class MailingSettingsListView(ListView):
    model = MailingSettings


class MailingSettingsDetailView(DetailView):
    model = MailingSettings


class MailingSettingsDeleteView(DeleteView):
    model = MailingSettings
    success_url = reverse_lazy('mailing:settings_list')


class MailingStatusListView(ListView):
    model = MailingStatus

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(owner=self.request.user)
        return queryset
