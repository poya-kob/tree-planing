from django import forms
from gallery.models import TreeImage


class TreeImageUploadForm(forms.ModelForm):
    class Meta:
        model = TreeImage
        fields = ['image']
        labels = {'image': 'انتخاب تصویر'}
        widgets = {
            'image': forms.FileInput(attrs={'class': 'form-control-file'})
        }
