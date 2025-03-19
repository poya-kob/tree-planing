from django import forms
from .models import Blog, Comment
from django_ckeditor_5.widgets import CKEditor5Widget


class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title', 'image', 'description', 'text', 'category']
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control", "placeholder": "عنوان مطلب را وارد کنید..."}),
            "image": forms.ClearableFileInput(attrs={"class": "form-control-file"}),
            "description": forms.Textarea(
                attrs={"class": "form-control", "rows": 3, "placeholder": "یک توضیح کوتاه بنویسید..."}),
            "text": CKEditor5Widget(attrs={"class": "django_ckeditor_5"}, config_name='extends'),  # ویجت CKEditor5

            "category": forms.Select(attrs={"class": "form-control"}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'email', 'text']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'نام شما'}),
            'email': forms.EmailInput(attrs={'placeholder': 'ایمیل شما'}),
            'text': forms.Textarea(attrs={'placeholder': 'متن نظر شما', 'rows': 3}),
        }

    def clean_text(self):
        text = self.cleaned_data.get('text')
        if len(text) > 500:  # محدودیت روی تعداد کاراکترها
            raise forms.ValidationError("حداکثر 500 کاراکتر می‌توانید وارد کنید.")
        return text
