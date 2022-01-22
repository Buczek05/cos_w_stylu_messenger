from django import forms
from . import models


class Message_form(forms.ModelForm):
    class Meta():
        model = models.Message
        fields = ('text',)
        labels = {
            'text':''
        }
        widgets = {
            'text': forms.TextInput(attrs={
                'type':'text',
                'class': 'text_message bg-dark text-white',
                'rows': '1',
                'onkeydown': 'pressed(event)',
                'placeholder': 'Aa',
                'autocomplete':'off'
            }),
        }
