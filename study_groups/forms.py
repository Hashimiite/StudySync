from django import forms
from .models import Message, SharedFile

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']
        widgets = {
            'content': forms.TextInput(attrs={'placeholder': 'Type your message...', 'class': 'form-control'}),
        }

class FileUploadForm(forms.ModelForm):
    class Meta:
        model = SharedFile
        fields = ['file']
