# accounts/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Field, Submit

class RegisterForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField()
    last_name = forms.CharField()
    date_of_birth = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        help_text="Your birth date",
    )

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "username",
            "email",
            "date_of_birth",
            "password1",
            "password2",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Initialize Crispy helper
        self.helper = FormHelper()
        self.helper.form_method = "post"
        # Add vertical spacing between fields
        self.helper.form_class = "space-y-6"

        # Define layout: each field, in order
        self.helper.layout = Layout(
            Fieldset(
                None,  # no visible fieldset legend
                Field("first_name"),
                Field("last_name"),
                Field("username"),
                Field("email"),
                Field("date_of_birth"),
                Field("password1"),
                Field("password2"),
            )
        )

        # Add a submit button with your Tailwind styling
        self.helper.add_input(
            Submit(
                "register",
                "Register",
                css_class=(
                    "w-full rounded-md bg-indigo-600 px-3.5 py-2.5 text-sm "
                    "font-semibold text-white shadow hover:bg-indigo-500"
                ),
            )
        )
