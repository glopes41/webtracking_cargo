from django import forms
from django.contrib.auth.models import User


class RegisterForm(forms.ModelForm):
    password2 = forms.CharField(
        label='Confirmação de Senha',
        required=True,
        widget=forms.PasswordInput(
            attrs={'placeholder': 'Digite novamente sua senha'}),
        help_text='Digite novamente a senha para confirmação.',
        error_messages={
            'required': 'A confirmação de senha é obrigatória.',
        }
    )

    class Meta:
        model = User
        fields = ['first_name', 'username', 'password']
        help_texts = {
            'username': 'O nome de usuário deve ser único.',
            'password': 'A senha deve ter pelo menos 8 caracteres.'
        }
        error_messages = {
            'username': {
                'unique': "Esse nome de usuário já existe. Escolha outro.",
            },
            'password': {
                'required': "A senha é obrigatória.",
            }
        }
        widgets = {
            'password': forms.PasswordInput(attrs={'placeholder': 'Digite sua senha', 'required': 'required'}),
            'first_name': forms.TextInput(attrs={'placeholder': 'Digite seu nome', 'required': 'required'}),
            'username': forms.TextInput(attrs={'placeholder': 'Digite um nome de usuário', 'required': 'required'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')
        username = cleaned_data.get('username')
        first_name = cleaned_data.get('first_name')

        if password and password2 and password != password2:
            self.add_error('password', "As senhas não coincidem.")
            self.add_error('password2', "As senhas não coincidem.")

        if len(password) < 3:
            self.add_error(
                'password', "A senha deve ter pelo menos 3 caracteres.")

        return cleaned_data
