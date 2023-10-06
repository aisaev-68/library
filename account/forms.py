from django import forms
from django.contrib.auth import password_validation

from account.models import User

style = "min-height: 45px; padding-left: 15px;"
margin_stile = "margin-top: 15px;"


class UserRegistrationForm(forms.ModelForm):
    """
    Класс формы регистрации пользователя.
    """

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['style'] = style

    username = forms.CharField(
        required=True,
        label='Пользователь*:',
        widget=forms.TextInput(
            attrs={
                'class': 'form-input',
                'placeholder': 'Пользователь*',
            }
        )
    )

    phone = forms.CharField(
        required=True,
        label='Номер телефона*:',
        widget=forms.TextInput(
            attrs={
                'class': 'form-input',
                'placeholder': 'Номер телефона*',
            }
        )
    )
    password1 = forms.CharField(
        required=True,
        label='Пароль*:',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-input',
                'placeholder': 'Пароль*',
            }
        ),
        help_text=password_validation.password_validators_help_text_html()
    )
    password2 = forms.CharField(
        required=True,
        label='Подтвердите пароль*:',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-input',
                'placeholder': 'Подтвердите пароль*',
            }
        )
    )
    email = forms.CharField(
        required=True,
        label='E-mail*:',
        widget=forms.EmailInput(
            attrs={
                'class': 'form-input',
                'placeholder': 'E-mail',
            }
        )
    )

    error_messages = {
        "password_mismatch": "Пароли не совпадают! Повторите ввод!",
        "phone_exists": "Пользователь с таким номером телефона уже существует!",
        "email_exists": "Пользователь с таким адресом электронной почты уже существует!",
    }

    class Meta:
        model = User
        fields = ('username', 'email', 'phone', 'password1', 'password2',)

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Пароли не совпадают! Повторите ввод!")

        return cleaned_data

    def clean_phone(self):
        """
        Метод для определение уникальности номера телефона.
        :return: phone
        """
        phone = self.cleaned_data.get('phone')
        if phone and User.objects.filter(phone=phone).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Этот номер телефона уже используется.")
        return phone

    def clean_email(self):
        """
        Метод для определения уникальности email.
        :return: email
        """
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Этот электронный адрес уже используется.")
        return email


class LoginForm(forms.Form):
    """
    Класс формы ввода пароля и логина.
    """
    username = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'class': 'form-input',
                'placeholder': 'Пользователь*',
            }
        ),
        required=True
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-input',
                'placeholder': 'Пароль*',
                'help_text': ''
            }
        )
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['style'] = style