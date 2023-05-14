from django.shortcuts import render , redirect
from app.forms import *
from django.contrib.auth.decorators import login_required
from django.views import View
from app.otp_service import send_otp
import requests
from django.db.models import Q
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

# Create your views here.

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = SignupForm()
    return render(request ,'app/signup.html',{'form':form})

# def login(request):
#     if request.method == 'POST':
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             print(form.cleaned_data)
#             mobile_num = 918777475206  #       038                          732
#             send_otp(1111,mobile_num)
#     else:
#         form = LoginForm()
#     return render(request ,'app/login.html',{'form':form})

@login_required()
def chat(request):
    current_user = request.user.username
    all_users = MyUser.objects.exclude(username=request.user.username)
    unseen = Chat.objects.filter(Q(receiver=request.user.username) & Q(is_seen=False)).all()
    chat_users = Chat.objects.filter(Q(sender=current_user) | Q(receiver=current_user)).all()
    context = { 'users': all_users,
                'chat_users':chat_users,
                'unseens':unseen
               }
    return render(request ,'app/chat.html' ,context=context)

@login_required()
def personal_chat(request,username):
    user_to = MyUser.objects.get(username=username)
    all_users = MyUser.objects.exclude(username=request.user.username)

    if request.user.id > user_to.id:
        group_name = f'chat_{user_to.id}-{request.user.id}'
    else:
        group_name = f'chat_{request.user.id}-{user_to.id}'

    
    unseen = Chat.objects.filter(Q(receiver=request.user.username) & Q(is_seen=False)).all()
    msgs = Chat.objects.filter(group_name=group_name)
    

    sender_user = user_to.username
    current_user = request.user.username

    chat_users = Chat.objects.filter(Q(sender=current_user) | Q(receiver=current_user)).all()

    Chat.objects.filter(receiver = current_user , sender = sender_user , group_name = group_name).update(is_seen = True)

    channel_layer = get_channel_layer()
    dict = {
            'from':sender_user,
            'num':'',
            'current_user':current_user,
            'status':'seen'
        }

    async_to_sync(channel_layer.group_send)('noti',
                                                 {"type": "chat_noti",
                                                  'data':dict
                                                  })

    context = {'users': all_users,
               'user_to':user_to,
               'messages':msgs,
               'chat_users':chat_users,
               'groupname':group_name,
               'unseens':unseen
               }
    return render(request, 'app/main chat.html' ,context=context)

