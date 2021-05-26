from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from django.utils.translation import gettext, gettext_lazy as _
from django.forms import ModelForm
from django.core.exceptions import ValidationError
import datetime
from .models import *


class UserFullName(User):
    class Meta:
        proxy = True
        ordering = ["last_name", "first_name"]

    def __str__(self):
        return self.get_full_name()


class bus_FullName(bus_model):
    class Meta:
        proxy = True
        ordering = ["gos_number"]

    def __str__(self):
        return f'{self.gos_number} - {self.marka}'


class station_Form(ModelForm):
    name = forms.CharField(label=_("Станция"), widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = station_model
        fields = ['name', ]


class bus_Form(ModelForm):
    marka = forms.CharField(label=_("Марка ТС"), widget=forms.TextInput(attrs={'class': 'form-control'}))
    gos_number = forms.CharField(label=_("Государственный номер"),
                                 widget=forms.TextInput(attrs={'class': 'form-control'}))
    place_count = forms.IntegerField(label=_("Число мест"), widget=forms.NumberInput(attrs={'class': 'form-control'}))

    class Meta:
        model = bus_model
        fields = ['marka', 'gos_number', 'place_count']


class flight_Form(ModelForm):
    start_id = forms.ModelChoiceField(label=_("Станция отправления"),
                                      widget=forms.Select(attrs={'class': 'form-control'}),
                                      queryset=None)
    finish_id = forms.ModelChoiceField(label=_("Станция прибытия"),
                                       widget=forms.Select(attrs={'class': 'form-control'}),
                                       queryset=None)
    date_start = forms.DateTimeField(label=_("Дата отправления"), widget=forms.DateTimeInput(
        attrs={'class': 'form-control', 'type': 'datetime-local'}))
    date_finish = forms.DateTimeField(label=_("Дата прибытия"), widget=forms.DateTimeInput(
        attrs={'class': 'form-control', 'type': 'datetime-local'}))
    bus_id = forms.ModelChoiceField(label=_("Автобус"), widget=forms.Select(attrs={'class': 'form-control'}),
                                    queryset=None)
    voditel_id = forms.ModelChoiceField(label=_("Водитель"), widget=forms.Select(attrs={'class': 'form-control'}),
                                        queryset=None)
    price = forms.IntegerField(label=_("Цена"), widget=forms.NumberInput(attrs={'class': 'form-control'}))

    class Meta:
        model = flight_model
        fields = ['start_id', 'finish_id', 'date_start', 'date_finish', 'bus_id', 'voditel_id', 'price']

    def __init__(self, *args, **kwargs):
        super(flight_Form, self).__init__(*args, **kwargs)
        self.fields['bus_id'].queryset = bus_FullName.objects.filter(is_delete=1)
        self.fields['start_id'].queryset = station_model.objects.filter(is_delete=1)
        self.fields['finish_id'].queryset = station_model.objects.filter(is_delete=1)
        self.fields['voditel_id'].queryset = UserFullName.objects.filter(groups__name='Водитель')

    def clean_price(self):
        data = self.cleaned_data['price']
        if int(data) < 0:
            raise ValidationError(_('Цена должна быть больше 0!'))
        return data

    def clean_date_start(self):
        data = self.cleaned_data['date_start']
        if data.date() < datetime.date.today():
            raise ValidationError(_('Дата не может быть прошлой!'))
        if data.date() > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(_('Вы не можете указать дату, на 4 недели вперед!'))
        return data

    def clean_date_finish(self):
        data = self.cleaned_data['date_finish']
        if data.date() < datetime.date.today():
            raise ValidationError(_('Дата не может быть прошлой!'))
        if data.date() > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(_('Вы не можете указать дату, на 4 недели вперед!'))
        return data


class cassir_ticket_Form(ModelForm):
    client_last_name = forms.CharField(label=_("Фамилия"), widget=forms.TextInput(attrs={'class': 'form-control'}))
    client_first_name = forms.CharField(label=_("Имя"), widget=forms.TextInput(attrs={'class': 'form-control'}))
    client_patronymic_name = forms.CharField(label=_("Отчесво"),
                                             widget=forms.TextInput(attrs={'class': 'form-control'}))
    client_birthday = forms.DateField(label=_("Дата рождения клиента"), widget=forms.DateTimeInput(
        attrs={'class': 'form-control', 'type': 'date'}))
    client_doc_series = forms.CharField(label=_("Серия документа"),
                                        widget=forms.TextInput(attrs={'class': 'form-control'}))
    client_doc_number = forms.CharField(label=_("Номер документа"),
                                        widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = flight_model
        fields = ['client_last_name', 'client_first_name', 'client_patronymic_name', 'client_birthday',
                  'client_doc_series', 'client_doc_number']