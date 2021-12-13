from dal import autocomplete

from django import forms
from .models import Channel,Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['channel','title','content']
        widgets = {
            'channel': autocomplete.ModelSelect2(url='channel-autocomplete')
        }
        

class ChannelUpdateForm(forms.ModelForm):
    channel_avatar = forms.ImageField(widget=forms.FileInput(attrs={'style':'display:none'}))
    channel_cover = forms.ImageField(widget=forms.FileInput(attrs={'style':'display:none'}))
    class Meta:
        model = Channel
        fields = ['channel_avatar','channel_cover','description']