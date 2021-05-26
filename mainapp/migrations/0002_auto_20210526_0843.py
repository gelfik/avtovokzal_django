# Generated by Django 3.1.2 on 2021-05-26 05:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket_model',
            name='client_birthday',
            field=models.DateField(blank=True, default=None, null=True, verbose_name='Дата рождения клиента'),
        ),
        migrations.AlterField(
            model_name='ticket_model',
            name='client_doc_number',
            field=models.CharField(blank=True, default=None, max_length=32, null=True, verbose_name='Номер документа'),
        ),
        migrations.AlterField(
            model_name='ticket_model',
            name='client_doc_series',
            field=models.CharField(blank=True, default=None, max_length=32, null=True, verbose_name='Серия документа'),
        ),
        migrations.AlterField(
            model_name='ticket_model',
            name='client_first_name',
            field=models.CharField(blank=True, default=None, max_length=256, null=True, verbose_name='Имя клиента'),
        ),
        migrations.AlterField(
            model_name='ticket_model',
            name='client_last_name',
            field=models.CharField(blank=True, default=None, max_length=256, null=True, verbose_name='Фамилия клиента'),
        ),
        migrations.AlterField(
            model_name='ticket_model',
            name='client_patronymic_name',
            field=models.CharField(blank=True, default=None, max_length=256, null=True, verbose_name='Отчесво клиента'),
        ),
    ]
