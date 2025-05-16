from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser,Files,Images

class CustomUserForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username','first_name','last_name','email','address','contact']

class FileForm(forms.ModelForm):
    class Meta:
        model = Files
        fields = ['file_name','file']

class ImageForm(forms.ModelForm):
    class Meta:
        model = Images
        fields = ['image_name','image']