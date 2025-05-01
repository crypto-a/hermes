#
# from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
# from django.contrib.auth.models import User
# from django import forms
# from django.contrib.auth.forms import UserCreationForm
# from crispy_forms.helper import FormHelper
# from crispy_forms.layout import Submit
#
# from .models import Profile
#
#
# # accounts/forms.p
#
#
#
# class ProfileForm(forms.ModelForm):
#     class Meta:
#         model = Profile
#         fields = ("picture", "date_of_birth")
#         widgets = {
#             "date_of_birth": forms.DateInput(attrs={'type': 'date'}),
#         }
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.helper = FormHelper()
#         self.helper.add_input(Submit("submit", "Save changes"))
