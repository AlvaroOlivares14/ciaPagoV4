from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
from .models import Post

class testeo(forms.ModelForm):
    email = forms.EmailField()
    username = forms.CharField(default=email)

    class Meta:
        model = User
        fields = ('email', 'username')