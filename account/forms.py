from django import forms
from .models import userProfile


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = userProfile
        fields = ['mobile','address']


class UpdateQuantityForm(forms.Form):
    quantity = forms.IntegerField(min_value=1 , label="Quantity")
    cart_item_id = forms.IntegerField(widget=forms.HiddenInput())


