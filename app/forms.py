from django import forms
from django.contrib.auth.forms import UserCreationForm 
from app.models import *
from django.core.exceptions import ValidationError

class SignupForm(UserCreationForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = MyUser
        fields = ['username','mobile_number', 'password1', 'password2']

    def clean_mobile_number(self):
        data = self.cleaned_data['mobile_number']
        if not data.isdigit():
            raise ValidationError('enter integer values')
        else:
            return data

class LoginForm(forms.Form):
    username = forms.CharField(max_length=255)
    mobile_number = forms.CharField()

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        mobile_num = cleaned_data.get("mobile_number")
        user = MyUser.objects.filter(username=username).exists()
        if not user:
            raise ValidationError('user does not exist')
        else:
            if not mobile_num.isdigit():
                raise ValidationError('enter integer values')
            elif len(mobile_num) != 10:
                raise ValidationError('mobile number must have 10 digits')
            else:
                user_mobile = MyUser.objects.get(username=username)
                if mobile_num != user_mobile.mobile_number:
                    raise ValidationError('you have entered wrong mobile number for user')
            