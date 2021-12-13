from django import forms
from django.contrib.auth.models import User
from .models import Profile

class UserUpdateForm(forms.ModelForm):
    email = forms.CharField(disabled=True)
    username = forms.CharField(disabled=True)
    class Meta:
        model = User
        fields = ['username','email']
        
class ProfileUpdateForm(forms.ModelForm):
    avatar = forms.ImageField(widget=forms.FileInput(attrs={'style':'display:none'}))
    cover = forms.ImageField(widget=forms.FileInput(attrs={'style':'display:none'}))
    class Meta:
        model = Profile
        fields = ['avatar','cover','description']