from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _


class UserForm(forms.ModelForm):
    _widget = forms.TextInput(attrs={'class': 'textInput'})
    email = forms.CharField(widget=_widget)
    first_name = forms.CharField(widget=_widget)
    last_name = forms.CharField(widget=_widget)
    # do not use password here since password, as a native field in
    # User Model, has certain encoding algorithm that a raw password
    # string wont fit. Therefore, we use password1 to get a raw
    # password and use set_password of User model to save it later
    password1 = forms.CharField(label=_('Password'),
                                widget=forms.PasswordInput(),
                                required=False)
    password2 = forms.CharField(label=_('Confirmation'),
                                widget=forms.PasswordInput(),
                                required=False)

    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        password1 = cleaned_data.get('password1', '')
        password2 = cleaned_data.get('password2', '')
        if password1 != password2:
            raise forms.ValidationError('Your passwords don\'t match')
        return cleaned_data

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name',
                  'password1', 'password2')


class RegistrationForm(forms.ModelForm):
    _widget = forms.TextInput(attrs={'class': 'textInput'})
    username = forms.CharField(widget=_widget)
    email = forms.CharField(widget=_widget)

    password1 = forms.CharField(label=_('Password'),
                                widget=forms.PasswordInput(),
                                required=False)
    password2 = forms.CharField(label=_('Confirmation'),
                                widget=forms.PasswordInput(),
                                required=False)

    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        password1 = cleaned_data.get('password1', '')
        password2 = cleaned_data.get('password2', '')
        if password1 != password2:
            raise forms.ValidationError('Your passwords don\'t match')
        return cleaned_data

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
