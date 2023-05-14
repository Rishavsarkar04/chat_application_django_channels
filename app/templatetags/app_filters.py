from django import template
from django.db.models import Q

register = template.Library()

@register.filter(name='filter_seen')
def filter_seen(query, sender):
    a = query.filter(sender=sender).all().count()
    if a==0:
        return ''
    return a  

@register.filter(name='filter_user_chat')
def filter_user_chat(query,user):
    print(user, 'filter')
    a = query.filter(Q(sender=user) | Q(receiver=user))
    if a.exists():
        return True
    else:
        return False    

