from django import forms
from django.contrib.auth import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm, Textarea, TextInput, widgets, PasswordInput


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        
        widgets = {
            'username': TextInput(attrs={
                'placeholder': 'Введите логин'
            }),
            
            'email': TextInput(attrs={
                'placeholder': 'Введите адрес электронной почты'
            }),
            
            'password1': TextInput(attrs={
                'type': 'password',
                'placeholder': 'Введите пароль'
            }),
            
            'password2': TextInput(attrs={
                'type': 'password',
                'placeholder': 'Повторите пароль'
            }),
        }
        
    def __init__(self, *args, **kwargs):
        super(CreateUserForm, self).__init__(*args, **kwargs)
        self.fields['password1'].widget = PasswordInput(attrs={'placeholder': 'Введите пароль'})
        self.fields['password2'].widget = PasswordInput(attrs={'placeholder': 'Повторите пароль'})
        
class UserLoginForm(AuthenticationForm, ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password')
