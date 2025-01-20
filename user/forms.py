from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from . models import Profile

class RegistrationForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput, label='Password')
    password2 = forms.CharField(widget=forms.PasswordInput, label='Confirm Password')

    class Meta:
        model = User
        fields = ['first_name', 'email', 'username', 'password1', 'password2']

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise ValidationError("The passwords do not match.")
        return password2


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['full_name', 'email', 'address', 'image', 'gender']

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        # Add 'form-control' class to all fields
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

        # Add extra class 'mt-2' to the gender field only
        self.fields['gender'].widget.attrs['class'] += ' mt-2'
