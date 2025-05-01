from django import forms
from django.contrib.auth.forms import AuthenticationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field

class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Username or E-mail")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # set up crispy helper
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.form_class = "space-y-6"           # vertical spacing between fields

        # make sure the default field labels / errors render
        # and then add a styled submit button
        self.helper.add_input(
            Submit(
                "login",
                "Log in",
                css_class=(
                    "w-full rounded-md bg-indigo-600 px-3.5 py-2.5 text-sm "
                    "font-semibold text-white shadow hover:bg-indigo-500"
                ),
            )
        )