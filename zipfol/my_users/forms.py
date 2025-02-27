from django import forms


class UsersFrom(forms.Form):
    phone = forms.CharField(widget=forms.TextInput(), label="موبایل")
    first_name = forms.CharField(widget=forms.TextInput(), label="نام")
    last_name = forms.CharField(widget=forms.TextInput(), label="نام خانوادگی")



