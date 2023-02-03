from django import forms
from .models import MessageModel, ServerMessageModel
class MForm(forms.ModelForm):

    class Meta:
        model = ServerMessageModel
        fields = ['text']