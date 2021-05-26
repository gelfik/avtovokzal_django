from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext, gettext_lazy as _


# Create your models here.


class station_model(models.Model):
    name = models.CharField('Станция', max_length=256, default=None)
    is_delete = models.BooleanField('Активен', default=True)

    class Meta:
        verbose_name = 'Станция'
        verbose_name_plural = 'Станции'
        db_table = 'station_model'

    def __str__(self):
        return self.name


class bus_model(models.Model):
    marka = models.CharField('Марка', max_length=256, default=None)
    gos_number = models.CharField('Гос номер', max_length=256, default=None)
    place_count = models.IntegerField('Мест', default=0)
    is_delete = models.BooleanField('Активен', default=True)

    class Meta:
        verbose_name = 'Автобус'
        verbose_name_plural = 'Автобусы'
        db_table = 'bus_model'

    def __str__(self):
        return self.gos_number

    def get_full_name(self):
        return f'{self.marka} - {self.gos_number}'


class flight_model(models.Model):
    bus_id = models.ForeignKey(bus_model, on_delete=models.CASCADE, verbose_name='Автобус',
                               default=None)
    start_id = models.ForeignKey(station_model, related_name='station_start', on_delete=models.CASCADE,
                                 verbose_name='Станция отправления',
                                 default=None)
    finish_id = models.ForeignKey(station_model, related_name='station_finish', on_delete=models.CASCADE,
                                  verbose_name='Станция прибытия',
                                  default=None)
    date_start = models.DateTimeField('Дата отправления', default=None)
    date_finish = models.DateTimeField('Дата прибытия', default=None)
    voditel_id = models.ForeignKey(User, related_name='voditels', on_delete=models.CASCADE, verbose_name='Водитель',
                                   default=None)
    price = models.FloatField('Цена', default=0)
    is_delete = models.BooleanField('Активен', default=True)

    class Meta:
        verbose_name = 'Рейс'
        verbose_name_plural = 'Рейсы'
        db_table = 'flight_model'

    def __str__(self):
        return f'{self.start_id} - {self.finish_id}'


class ticket_model(models.Model):
    flight_id = models.ForeignKey(flight_model, on_delete=models.CASCADE, verbose_name='Рейс', default=None)
    cashier_id = models.ForeignKey(User, related_name='cashiers', on_delete=models.CASCADE, verbose_name='Кассир',
                                   default=None, null=True, blank=True)
    place = models.IntegerField('Место', default=0)
    buy_time = models.DateTimeField('Время покупки', auto_now=True)

    is_buy = models.BooleanField('Статус покупки', default=False)
    is_pay = models.BooleanField('Статус оплаты', default=False)

    client_last_name = models.CharField('Фамилия клиента', max_length=256, default=None, null=True, blank=True)
    client_first_name = models.CharField('Имя клиента', max_length=256, default=None, null=True, blank=True)
    client_patronymic_name = models.CharField('Отчесво клиента', max_length=256, default=None, null=True, blank=True)
    client_birthday = models.DateField('Дата рождения клиента', default=None, null=True, blank=True)
    client_doc_series = models.CharField('Серия документа', max_length=32, default=None, null=True, blank=True)
    client_doc_number = models.CharField('Номер документа', max_length=32, default=None, null=True, blank=True)

    is_delete = models.BooleanField('Активен', default=True)

    class Meta:
        verbose_name = 'Билет'
        verbose_name_plural = 'Билеты'
        db_table = 'ticket_model'

    def __str__(self):
        return f'{self.id}'

    def get_client_fio(self):
        return f'{self.client_last_name} {self.client_first_name} {self.client_patronymic_name}'

    def get_client_doc(self):
        return f'{self.client_doc_series}-{self.client_doc_number}'