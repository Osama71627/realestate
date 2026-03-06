from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, label='الاسم الأول',
        widget=forms.TextInput(attrs={'placeholder': 'الاسم الأول', 'class': 'form-input'}))
    last_name = forms.CharField(max_length=30, required=True, label='اسم العائلة',
        widget=forms.TextInput(attrs={'placeholder': 'اسم العائلة', 'class': 'form-input'}))
    email = forms.EmailField(required=True, label='البريد الإلكتروني',
        widget=forms.EmailInput(attrs={'placeholder': 'example@email.com', 'class': 'form-input'}))
    username = forms.CharField(label='اسم المستخدم',
        widget=forms.TextInput(attrs={'placeholder': 'اسم المستخدم', 'class': 'form-input'}))
    password1 = forms.CharField(label='كلمة المرور',
        widget=forms.PasswordInput(attrs={'placeholder': '••••••••', 'class': 'form-input'}))
    password2 = forms.CharField(label='تأكيد كلمة المرور',
        widget=forms.PasswordInput(attrs={'placeholder': '••••••••', 'class': 'form-input'}))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('هذا البريد الإلكتروني مسجل مسبقاً')
        return email


class LoginForm(AuthenticationForm):
    username = forms.CharField(label='اسم المستخدم',
        widget=forms.TextInput(attrs={'placeholder': 'اسم المستخدم', 'class': 'form-input', 'autofocus': True}))
    password = forms.CharField(label='كلمة المرور',
        widget=forms.PasswordInput(attrs={'placeholder': '••••••••', 'class': 'form-input'}))
