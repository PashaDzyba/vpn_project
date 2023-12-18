from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, Profile
from django import forms
from django.contrib.auth.hashers import make_password


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('email', 'first_name', 'last_name',)


class ProfileForm(forms.ModelForm):
    email = forms.EmailField(required=False)  # Add email field
    first_name = forms.CharField(required=False)  # Add first name field
    last_name = forms.CharField(required=False)  # Add last name field
    password = forms.CharField(widget=forms.PasswordInput(), required=False)  # Add password field

    class Meta:
        model = Profile
        fields = ['avatar', 'email', 'first_name', 'last_name', 'password']

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.user:
            self.fields['email'].initial = self.instance.user.email
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name

    def save(self, commit=True):
        profile = super(ProfileForm, self).save(commit=False)
        if self.cleaned_data['email']:
            profile.user.email = self.cleaned_data['email']
        if self.cleaned_data['first_name']:
            profile.user.first_name = self.cleaned_data['first_name']
        if self.cleaned_data['last_name']:
            profile.user.last_name = self.cleaned_data['last_name']
        if self.cleaned_data['password']:
            profile.user.password = make_password(self.cleaned_data['password'])

        if commit:
            profile.user.save()
            profile.save()
        return profile
