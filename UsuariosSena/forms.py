# #prueba loginnnnnnnnnnnnn
# from django import forms

from django import forms
from .models import (
    UsuariosSena,
    ElementosDevolutivo,
    ElementosConsumible,
    Prestamo,
    EntregaConsumible,
)
from django.forms import ModelForm


class UsuariosSenaForm(forms.ModelForm):
    class Meta:
        model = UsuariosSena
        fields = "__all__"


class UserLoginForm(forms.Form):
    numeroIdentificacion = forms.CharField(label="numeroIdentificacion")
    password = forms.CharField(widget=forms.PasswordInput, label="password")


class ElementosDevolutivoForm(forms.ModelForm):
    class Meta:
        model = ElementosDevolutivo
        fields = "__all__"


class ElementosConsumiblesForm(forms.ModelForm):
    class Meta:
        model = ElementosConsumible
        fields = "__all__"


class PrestamosForm(forms.ModelForm):
    class Meta:
        model = Prestamo
        fields = "__all__"


class EntregaConsumibleForm(forms.ModelForm):
    class Meta:
        model = EntregaConsumible
        fields = "__all__"
