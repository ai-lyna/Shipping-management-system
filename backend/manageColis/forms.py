from django import forms
from .models import Colis


class ColisForm(forms.ModelForm):
    class Meta:
        model = Colis
        fields="__all__"
