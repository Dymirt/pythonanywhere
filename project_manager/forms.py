from django.forms import ModelForm, PasswordInput, TextInput
from .models import Organization


class OrganizationLoginForm(ModelForm):
    class Meta:
        model = Organization
        fields = ["login", "password"]
        widgets = {
            "login": TextInput(
                attrs={
                    "name": "Login",
                    "class": "form-control mb-3",
                }
            ),
            "password": PasswordInput(
                attrs={
                    "name": "Password",
                    "class": "form-control mb-3",
                }
            ),
        }
