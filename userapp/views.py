from .forms import *
from mainapp.views import *

# Create your views here.
def login(request):
    arguments = {}
    arguments.update(csrf(request))
    arguments.update(form=UserLoginForm)
    if request.user.is_authenticated:
        return redirect(reverse('main_url'))
    if request.method == 'GET':
        arguments.update(next=request.GET['next'] if request.GET and 'next' in request.GET else '')
        return render(request, 'userapp/login.html', {'arguments': arguments})
    elif request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        userdata = auth.authenticate(username=username, password=password)
        try:
            usersearch = User.objects.get(username=username)
        except Exception as e:
            print(e)
            usersearch = None
        if userdata is not None:
            auth.login(request, userdata)
            next_url = request.POST.get('next', '')
            if next_url != '':
                return redirect(next_url)
            else:
                return redirect(reverse('main_url'))
        elif usersearch is not None:
            arguments.update(error='Не верный пароль!')
            return render(request, 'userapp/login.html', {'arguments': arguments})
        else:
            arguments.update(error='Пользователь не найден!')
            return render(request, 'userapp/login.html', {'arguments': arguments})
    else:
        return HttpResponse('405 Method Not Allowed', status=405)


def logout(request):
    auth.logout(request)
    return redirect('/')

# def register(request):
#     arguments = {}
#     arguments.update(csrf(request))
#     arguments.update(form=UserRegisterForm)
#     if request.user.is_authenticated:
#         return redirect(reverse('main_url'))
#     if request.method == 'GET':
#         arguments.update(next=request.GET['next'] if request.GET and 'next' in request.GET else '')
#         return render(request, 'userapp/register.html', {'arguments': arguments})
#     elif request.method == 'POST':
#         newuser_form = UserRegisterForm(request.POST)
#         if newuser_form.is_valid():
#             userform = newuser_form.save()
#             userform.refresh_from_db()
#             userform.groups.clear()
#             userform.groups.add(newuser_form.cleaned_data.get('group_data'))
#             userform.set_password(newuser_form.cleaned_data['password2'])
#             userform.save()
#             auth.login(request, userform)
#             next_url = request.POST.get('next', '')
#             if next_url != '':
#                 return redirect(next_url)
#             return redirect(reverse('main_url'))
#         else:
#             arguments.update(form=UserRegisterForm(request.POST))
#             arguments.update(error='Форма заполнена не корректно!')
#             return render(request, 'userapp/register.html', {'arguments': arguments})
#     else:
#         return HttpResponse('405 Method Not Allowed', status=405)

def register(request):
    arguments = {}
    arguments.update(csrf(request))
    if request.user.is_authenticated and has_group(request.user, 'Диспетчер'):
        if request.method == 'POST':
            newuser_form = UserRegisterForm(request.POST)
            if newuser_form.is_valid():
                new_password = gen_one_password(10)
                new_username = transliterate(
                    newuser_form.cleaned_data.get('first_name')[:1] + newuser_form.cleaned_data.get('last_name'))
                user_in_bd = True
                count = 1
                while user_in_bd:
                    if count == 1 and not User.objects.filter(username=new_username).exists():
                        user_in_bd = False
                    elif not User.objects.filter(username=f'{new_username}{count}').exists():
                        user_in_bd = False
                        new_username = f'{new_username}{count}'
                    else:
                        count += 1
                userform = newuser_form.save(username=new_username, password=new_password)
                userform.refresh_from_db()
                userform.last_name = newuser_form.cleaned_data.get('last_name')
                userform.first_name = newuser_form.cleaned_data.get('first_name')
                userform.email = newuser_form.cleaned_data.get('email')
                userform.groups.clear()
                userform.groups.add(newuser_form.cleaned_data.get('group_data'))
                userform.set_password(new_password)
                userform.save()
                mydata.set_register(new_username,new_password)
                return redirect(reverse('user_list_url'))
            else:
                mydata.set_error('Форма добавления сотрудника заполнена не корректно!')
                return redirect(reverse('user_list_url'))
        else:
            return HttpResponse('405 Method Not Allowed', status=405)
    else:
        return redirect('/')