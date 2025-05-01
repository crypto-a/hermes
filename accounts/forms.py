from django import forms
from django.contrib.auth.models import User


class RegisterForm(forms.ModelForm):
    name = forms.CharField(max_length=150, label="Full name")
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ("username", "email", "name", "password")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data["name"]
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    identifier = forms.CharField(label="Username or Email")
    password = forms.CharField(widget=forms.PasswordInput)
