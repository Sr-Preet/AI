from django import forms
from myapp.models import Image, Chatter


class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('img',)


class ChatterForm(forms.ModelForm):
    class Meta:
        model = Chatter
        fields = ('txt',)
