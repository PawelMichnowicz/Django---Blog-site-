from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm
from django.forms.widgets import ClearableFileInput, FileInput

from account.models import Profile


class RegisterForm(forms.ModelForm):
    # form for registration 
    password = forms.CharField(label='hasło', widget=forms.PasswordInput)
    password2 = forms.CharField(label='powtórz hasło', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email')
        help_texts = {'username': None,}
        error_messages={
            'username' : {'unique': ("Nazwa użytkownika zajęta")}, 
            'email' : {'invalid': ("Wprowadź poprawny adres email")}} # change communication for polish language

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError("Hasła różnią się od siebie")
        return cd['password2']


class ProfileForm(forms.ModelForm):
    # create profile(one-to-one relationg with User) form to be able to add image avatar 
    class Meta:
        model = Profile
        fields = ['image']
        help_texts = {
            'image': "Opcjonalne",
        }

class ProfileEditForm(forms.ModelForm):
    # create profile edit form to be able to edit image avatar
    image = forms.ImageField(widget=FileInput, label='Zmień Avatar')
    class Meta:
        model = Profile
        fields = ('image',)


class MyAuthForm(AuthenticationForm):
    error_messages = {
        'invalid_login': (
            "Nieprawidłowa nazwa użytkownika lub hasło " # change communication during authentication to polish language
        ),
        'inactive': ("Konto jest nieaktywne"),
    }

class MyLoginView(LoginView): # add changed communication to authentication process
    authentication_form = MyAuthForm 