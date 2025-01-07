from django import forms
from .models import userProfile


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = userProfile
        fields = ['mobile','address']