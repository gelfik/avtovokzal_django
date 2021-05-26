from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template.context_processors import csrf
from django.contrib.auth.models import User, Group
from django.contrib import auth
from django.utils import timezone
from .models import *
from django.urls import reverse
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .forms import *
from userapp.forms import *


def has_group(user, group_name):
    from django.contrib.auth.models import Group
    group = Group.objects.get(name=group_name)
    return True if group in user.groups.all() else False


def gen_one_password(lenght):
    if lenght <= 8:
        x = 1
    elif 8 < lenght <= 12:
        x = 2
    else:
        x = 3
    import random, string
    Pass_Symbol = []
    spec_cymbol = []
    result = []
    spec_cymbol.extend(list("!#$%&()*+-<=>?"))
    Pass_Symbol.extend(list(string.ascii_letters + string.digits))
    psw = ''.join([random.choice(Pass_Symbol) for x in range(int(lenght - x))]) + ''.join(
        [random.choice(spec_cymbol) for x in range(int(x))])
    result.extend(list(psw))
    random.shuffle(result)
    return "".join(result)


def transliterate(name):
    slovar = {'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'e',
              'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'i', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n',
              'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'h',
              'ц': 'c', 'ч': 'cz', 'ш': 'sh', 'щ': 'scz', 'ъ': '', 'ы': 'y', 'ь': '', 'э': 'e',
              'ю': 'u', 'я': 'ja', 'А': 'A', 'Б': 'B', 'В': 'V', 'Г': 'G', 'Д': 'D', 'Е': 'E', 'Ё': 'E',
              'Ж': 'ZH', 'З': 'Z', 'И': 'I', 'Й': 'I', 'К': 'K', 'Л': 'L', 'М': 'M', 'Н': 'N',
              'О': 'O', 'П': 'P', 'Р': 'R', 'С': 'S', 'Т': 'T', 'У': 'U', 'Ф': 'F', 'Х': 'H',
              'Ц': 'C', 'Ч': 'CZ', 'Ш': 'SH', 'Щ': 'SCH', 'Ъ': '', 'Ы': 'y', 'Ь': '', 'Э': 'E',
              'Ю': 'U', 'Я': 'YA', ',': '', '?': '', ' ': '_', '~': '', '!': '', '@': '', '#': '',
              '$': '', '%': '', '^': '', '&': '', '*': '', '(': '', ')': '', '-': '', '=': '', '+': '',
              ':': '', ';': '', '<': '', '>': '', '\'': '', '"': '', '\\': '', '/': '', '№': '',
              '[': '', ']': '', '{': '', '}': '', 'ґ': '', 'ї': '', 'є': '', 'Ґ': 'g', 'Ї': 'i',
              'Є': 'e', '—': ''}
    for key in slovar:
        name = name.replace(key, slovar[key])
    return name


class MyData:
    error_message = ''
    error_status = False
    register_login = ''
    register_password = ''
    register_status = False
    form = None

    def set_error(self, error_message, form):
        self.error_message = error_message
        self.error_status = True
        self.form = form

    def set_register(self, register_login, register_password):
        self.register_login = register_login
        self.register_password = register_password
        self.register_status = True

    def get_error(self):
        self.error_status = False
        return f'{self.error_message}', self.form

    def get_error_status(self):
        return self.error_status

    def get_register(self):
        self.register_status = False
        return f'{self.register_login}', f'{self.register_password}'

    def get_register_status(self):
        return self.register_status


mydata = MyData()


# Create your views here.

@login_required
def index(request):
    arguments = {}
    arguments.update(csrf(request))
    if request.user.is_authenticated:
        if has_group(request.user, 'Водитель'):
            if request.method == "GET":
                arguments.update(
                    flight_list=flight_model.objects.filter(is_delete=1, voditel_id=request.user,
                                                            date_start__gte=timezone.now()).order_by(
                        'date_start', 'date_finish'))
                q_start = request.GET.get('q_start', None)
                q_finish = request.GET.get('q_finish', None)
                if q_start is not None and q_finish is not None:
                    arguments.update(
                        flight_list=flight_model.objects.filter(is_delete=1, voditel_id=request.user,
                                                                start_id__name__contains=q_start,
                                                                finish_id__name__contains=q_finish).order_by(
                            'date_start', 'date_finish'))
                    arguments.update(query_start_data=q_start)
                    arguments.update(query_finish_data=q_finish)
                elif q_start is not None:
                    arguments.update(
                        flight_list=flight_model.objects.filter(is_delete=1, voditel_id=request.user,
                                                                start_id__name__contains=q_start).order_by('date_start',
                                                                                                           'date_finish'))
                    arguments.update(query_start_data=q_start)
                elif q_finish is not None:
                    arguments.update(
                        flight_list=flight_model.objects.filter(is_delete=1, voditel_id=request.user,
                                                                finish_id__name__contains=q_finish).order_by(
                            'date_start', 'date_finish'))
                    arguments.update(query_finish_data=q_finish)
                if mydata.error_status:
                    error_message, form = mydata.get_error()
                    arguments.update(error=error_message)
                return render(request, 'mainapp/voditel/index.html', {'arguments': arguments})
            else:
                return HttpResponse('405 Method Not Allowed', status=405)
        elif has_group(request.user, 'Кассир'):
            if request.method == "GET":
                arguments.update(form=cassir_ticket_Form)
                arguments.update(
                    flight_list=flight_model.objects.filter(is_delete=1, date_start__gte=timezone.now()).order_by(
                        'date_start', 'date_finish'))
                q_start = request.GET.get('q_start', None)
                q_finish = request.GET.get('q_finish', None)
                if q_start is not None and q_finish is not None:
                    arguments.update(
                        flight_list=flight_model.objects.filter(is_delete=1, start_id__name__contains=q_start,
                                                                finish_id__name__contains=q_finish).order_by(
                            'date_start', 'date_finish'))
                    arguments.update(query_start_data=q_start)
                    arguments.update(query_finish_data=q_finish)
                elif q_start is not None:
                    arguments.update(
                        flight_list=flight_model.objects.filter(is_delete=1, start_id__name__contains=q_start).order_by(
                            'date_start',
                            'date_finish'))
                    arguments.update(query_start_data=q_start)
                elif q_finish is not None:
                    arguments.update(
                        flight_list=flight_model.objects.filter(is_delete=1,
                                                                finish_id__name__contains=q_finish).order_by(
                            'date_start', 'date_finish'))
                    arguments.update(query_finish_data=q_finish)
                if mydata.error_status:
                    error_message, form = mydata.get_error()
                    arguments.update(error=error_message)
                return render(request, 'mainapp/cashier/index.html', {'arguments': arguments})
            else:
                return HttpResponse('405 Method Not Allowed', status=405)
        elif has_group(request.user, 'Диспетчер'):
            if request.method == "GET":
                arguments.update(form=flight_Form)
                if mydata.error_status:
                    error_message, form = mydata.get_error()
                    arguments.update(error=error_message)
                    arguments.update(form=form)
                arguments.update(
                    flight_list=flight_model.objects.filter(is_delete=1, date_start__gte=timezone.now()).order_by(
                        'date_start', 'date_finish'))
                q_start = request.GET.get('q_start', None)
                q_finish = request.GET.get('q_finish', None)
                # q_data_start = request.GET.get('q_data_start', None)
                if q_start is not None and q_finish is not None:
                    arguments.update(
                        flight_list=flight_model.objects.filter(is_delete=1, start_id__name__contains=q_start,
                                                                finish_id__name__contains=q_finish).order_by(
                            'date_start', 'date_finish'))
                    arguments.update(query_start_data=q_start)
                    arguments.update(query_finish_data=q_finish)
                elif q_start is not None:
                    arguments.update(
                        flight_list=flight_model.objects.filter(is_delete=1,
                                                                start_id__name__contains=q_start).order_by('date_start',
                                                                                                           'date_finish'))
                    arguments.update(query_start_data=q_start)
                elif q_finish is not None:
                    arguments.update(
                        flight_list=flight_model.objects.filter(is_delete=1,
                                                                finish_id__name__contains=q_finish).order_by(
                            'date_start', 'date_finish'))
                    arguments.update(query_finish_data=q_finish)

                return render(request, 'mainapp/dispatcher/index.html', {'arguments': arguments})
            else:
                return HttpResponse('405 Method Not Allowed', status=405)
        else:
            return redirect(reverse('logout_url'))
    else:
        return HttpResponse('405 Method Not Allowed', status=405)


@login_required
def flight_edit_views(request):
    if has_group(request.user, 'Диспетчер'):
        if request.method == "POST":
            new_form = flight_Form(request.POST)
            if new_form.is_valid():
                new_data = new_form.save()
                for i in range(new_data.bus_id.place_count):
                    new_ticket = ticket_model.objects.create(flight_id=new_data, place=i + 1)
                    new_ticket.save()
            else:
                mydata.set_error('Форма доавления рейса заполнена не корректно!', flight_Form(request.POST))
            return redirect(reverse('main_url'))
        else:
            return HttpResponse('405 Method Not Allowed', status=405)
    else:
        return redirect(reverse('main_url'))


@login_required
def flight_views(request, flight_id):
    arguments = {}
    if has_group(request.user, 'Диспетчер'):
        if request.method == "GET":
            try:
                arguments.update(flight=flight_model.objects.get(id=flight_id, is_delete=1))
                arguments.update(ticket_list=ticket_model.objects.filter(flight_id_id=flight_id, is_delete=1))
            except:
                return redirect(reverse('main_url'))
            return render(request, 'mainapp/dispatcher/flight.html', {'arguments': arguments})
        else:
            return HttpResponse('405 Method Not Allowed', status=405)
    elif has_group(request.user, 'Водитель'):
        if request.method == "GET":
            try:
                arguments.update(flight=flight_model.objects.get(id=flight_id, is_delete=1, voditel_id=request.user))
                arguments.update(ticket_list=ticket_model.objects.filter(flight_id_id=flight_id, is_delete=1))
            except:
                return redirect(reverse('main_url'))
            return render(request, 'mainapp/voditel/flight.html', {'arguments': arguments})
        else:
            return HttpResponse('405 Method Not Allowed', status=405)
    else:
        return redirect(reverse('main_url'))


@login_required
def bus_views(request):
    arguments = {}
    arguments.update(csrf(request))
    if request.user.is_authenticated and has_group(request.user, 'Диспетчер'):
        if request.method == "GET":
            arguments.update(form=bus_Form)
            if mydata.error_status:
                error_message, form = mydata.get_error()
                arguments.update(error=error_message)
                arguments.update(form=form)
            arguments.update(
                bus_list=bus_model.objects.filter(is_delete=1).order_by('gos_number'))
            return render(request, 'mainapp/dispatcher/bus.html', {'arguments': arguments})
        elif request.method == "POST":
            new_form = bus_Form(request.POST)
            if new_form.is_valid():
                new_form.save()
            else:
                mydata.set_error('Форма доавления автобуса заполнена не корректно!', bus_Form(request.POST))
            return redirect(reverse('bus_list_url'))
        else:
            return HttpResponse('405 Method Not Allowed', status=405)
    else:
        return redirect(reverse('main_url'))


@login_required
def bus_edit_views(request, bus_id, method):
    arguments = {}
    arguments.update(csrf(request))
    if request.user.is_authenticated and has_group(request.user, 'Диспетчер'):
        if request.method == "GET":
            if method == 'delete':
                try:
                    dus_object = bus_model.objects.get(is_delete=1, id=bus_id)
                    dus_object.is_delete = 0
                    dus_object.save()
                except:
                    pass
            return redirect(reverse('bus_list_url'))
        else:
            return HttpResponse('405 Method Not Allowed', status=405)
    else:
        return redirect(reverse('main_url'))


@login_required
def user_list_views(request):
    arguments = {}
    arguments.update(csrf(request))
    arguments.update(form=UserRegisterForm)
    arguments.update(user_list=User.objects.filter(is_active=1).order_by('-last_name').order_by('-first_name'))
    user_edit = []
    for i, item in enumerate(arguments['user_list']):
        user_edit.append({'form': UserRegisterForm(instance=item), 'id': item.id})
    arguments.update(user_edit=user_edit)
    if request.user.is_authenticated and has_group(request.user, 'Диспетчер'):
        if request.method == "GET":
            if mydata.get_register_status():
                new_username, new_password = mydata.get_register()
                arguments.update(add_user_data={'password': new_password, 'username': new_username})
            if mydata.get_error_status():
                error_message, form = mydata.get_error()
                arguments.update(error=error_message)
            return render(request, 'mainapp/dispatcher/user.html', {'arguments': arguments})
        else:
            return HttpResponse('405 Method Not Allowed', status=405)
    else:
        return redirect(reverse('main_url'))


@login_required
def user_edit_views(request, user_id, method):
    arguments = {}
    arguments.update(csrf(request))
    if request.user.is_authenticated and has_group(request.user, 'Диспетчер'):
        if request.method == "GET":
            if method == 'delete':
                try:
                    usr_object = User.objects.get(is_active=1, id=user_id)
                    usr_object.is_active = 0
                    usr_object.save()
                except:
                    mydata.set_error('Сотрудник не найден!', None)
            return redirect(reverse('user_list_url'))
        elif request.method == "POST":
            if method == 'edit':
                try:
                    usr_object = User.objects.get(is_active=1, id=user_id)
                    new_form = UserRegisterForm(request.POST, instance=usr_object)
                    if new_form.is_valid():
                        usr_object.first_name = new_form.cleaned_data.get('first_name')
                        usr_object.last_name = new_form.cleaned_data.get('last_name')
                        usr_object.email = new_form.cleaned_data.get('email')
                        usr_object.groups.clear()
                        usr_object.groups.add(new_form.cleaned_data.get('group_data'))
                        usr_object.save()
                    else:
                        mydata.set_error('Форма редактирвоания заполнена не корректно!', None)
                    return redirect(reverse('user_list_url'))
                except:
                    mydata.set_error('Сотрудник не найден!', None)
                    return redirect(reverse('user_list_url'))
            return redirect(reverse('user_list_url'))
        else:
            return HttpResponse('405 Method Not Allowed', status=405)
    else:
        return redirect(reverse('main_url'))


@login_required
def sell_views(request, flight_id):
    arguments = {}
    if has_group(request.user, 'Кассир'):
        if request.method == "POST":
            try:
                flight_object = flight_model.objects.get(id=flight_id, is_delete=1)
                arguments.update(flight=flight_object)
                ticket_object = ticket_model.objects.filter(flight_id=flight_object, is_delete=1, is_buy=0).first()
                arguments.update(ticket=ticket_object)
                new_form = cassir_ticket_Form(request.POST, instance=ticket_object)
                if new_form.is_valid():
                    ticket_object.client_last_name = new_form.cleaned_data.get('client_last_name')
                    ticket_object.last_name = new_form.cleaned_data.get('client_first_name')
                    ticket_object.client_patronymic_name = new_form.cleaned_data.get('client_patronymic_name')
                    ticket_object.client_birthday = new_form.cleaned_data.get('client_birthday')
                    ticket_object.client_doc_series = new_form.cleaned_data.get('client_doc_series')
                    ticket_object.client_doc_number = new_form.cleaned_data.get('client_doc_number')
                    ticket_object.cashier_id = request.user
                    ticket_object.is_buy = 1
                    ticket_object.is_pay = 1
                    ticket_object.save()
                    return redirect(reverse('ticket_url', args=[ticket_object.id]))
                else:
                    mydata.set_error('Форма продажи заполнена не корректно!', None)
                    return redirect(reverse('main_url'))
            except:
                return redirect(reverse('main_url'))
        else:
            return HttpResponse('405 Method Not Allowed', status=405)
    else:
        return redirect(reverse('main_url'))


@login_required
def ticket_views(request, ticket_id):
    arguments = {}
    if has_group(request.user, 'Кассир'):
        if request.method == "GET":
            try:
                ticket_object = ticket_model.objects.get(id=ticket_id, is_delete=1)
                arguments.update(ticket=ticket_object)
                return render(request, 'mainapp/cashier/ticket.html', {'arguments': arguments})
            except:
                return redirect(reverse('main_url'))
        else:
            return HttpResponse('405 Method Not Allowed', status=405)
    else:
        return redirect(reverse('main_url'))
