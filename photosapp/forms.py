from django import forms
from .models import Profile, Photo

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'profile_picture']

class PhotoUploadForm(forms.ModelForm):
    tags = forms.CharField(required=False, help_text='Comma-separated tags')

    class Meta:
        model = Photo
        fields = ['title', 'description', 'image', 'tags']