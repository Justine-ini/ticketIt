from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Ticket, Company, Sector
from .models import UserProfile


class CreateUserForm(UserCreationForm):
  class Meta:
    model = User
    fields = ["username", "email", "password1", "password2"]


class UserProfileForm(ModelForm):
  class Meta:

    models = UserProfile
    fields = '__all__'


class AddcompanyForm(forms.ModelForm):
  class Meta:
    model = Company
    fields = ["name"]

class TicketForm(ModelForm):
  # recipient_email = forms.EmailField()  # Add this field and set disabled=True
  recipient_email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'placeholder': "The recipient's email is auto-filled after a system search"
        })
    )

  class Meta:
    model = Ticket
    fields = ['title', 'user_email', 'recipient_email', 'company', 'sector', 'description']
    widgets = {
        'description': forms.Textarea(attrs={'rows': 4}),
    }




class AddsectorForm(forms.ModelForm):
  class Meta:
    model = Sector
    fields = ["name"]


