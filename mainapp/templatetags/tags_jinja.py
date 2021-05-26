from django import template
from django.contrib.auth.models import Group
from mainapp.models import *

register = template.Library()

@register.filter(name='has_group')
def has_group(user, group_name):
    group = Group.objects.get(name=group_name)
    return True if group in user.groups.all() else False

@register.filter(name='cheak_count_list')
def cheak_count_list(list):
    try:
        if len(list) > 0:
            return True
        else:
            return False
    except:
        return False

@register.filter(name='get_count_place')
def get_count_place(flight):
    try:
        return f'{ticket_model.objects.filter(flight_id=flight, is_buy=0).count()}/{ticket_model.objects.filter(flight_id=flight).count()}'
    except:
        return '0/0'