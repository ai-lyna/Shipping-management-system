from django import forms
from .models import Expedition, Facture, Tournee


class ExpeditionForm(forms.ModelForm):
    class Meta:
        model = Expedition
        fields="__all__"


class TourneeForm(forms.ModelForm):
    class Meta:
        model = Tournee
        fields="__all__"



class FactureForm(forms.ModelForm):
    class Meta:
        model = Facture
        fields="__all__"