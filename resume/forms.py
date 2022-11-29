from .models import Message

from django.forms import ModelForm, CharField, TextInput

class MessageFrom(ModelForm):

    class Meta:
        model = Message
        fields = ['name', 'email', 'message']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].label = ''
        self.fields['name'].widget.attrs.update({'class': 'form-control scroll-animated-from-right',
                                                 'id': "contact-form-name",
                                                 'placeholder': "* Your Name"})
        self.fields['email'].label = ''
        self.fields['email'].widget.attrs.update({'class': 'form-control scroll-animated-from-right',
                                                 'id': "contact-form-email",
                                                 'placeholder': "* Your Email"})
        self.fields['message'].label = ''
        self.fields['message'].widget.attrs.update({'class': 'form-control scroll-animated-from-right',
                                                 'id': "contact-form-message",
                                                 'placeholder': "* Your Message"})