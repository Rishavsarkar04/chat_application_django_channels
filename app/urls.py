from django.urls import path,include
from app import views
from django.contrib.auth import views as auth_views
from app.forms import LoginForm
urlpatterns = [
    path('', views.signup , name='signup'),
    path('signup/', views.signup , name='signup'),

    # path('login/', views.login , name='login'),
    path('login/', auth_views.LoginView.as_view(template_name = 'app/login.html',next_page='chat') , name='login'),
    path('logout', auth_views.LogoutView.as_view(next_page='login') , name='logout'),

    path('chat/', views.chat , name='chat'),
    path('chat/<str:username>', views.personal_chat , name='personal_chat'),
]