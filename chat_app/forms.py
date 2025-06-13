from django.forms import Form, CharField

class MessageForm(Form):
    message = CharField(
        max_length= 255,
        label='Entry a message',
        
    )