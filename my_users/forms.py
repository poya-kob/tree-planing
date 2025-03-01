from django import forms


class UsersFrom(forms.Form):
    phone = forms.CharField(widget=forms.TextInput(attrs={'class': 'formbold-form-input', 'placeholder': 'موبایل'}),
                            label="موبایل")
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'formbold-form-input', 'placeholder': 'نام'}),
                                 label="نام")
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'formbold-form-input', 'placeholder': 'نام خانوادگی'}),
        label="نام خانوادگی")
    stage = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'formbold-form-input', 'placeholder': 'مقطع تحصیلی'}),
        label='مقطع تحصیلی')
    school = forms.CharField(widget=forms.TextInput(attrs={'class': 'formbold-form-input', 'placeholder': 'نام مدرسه'}),
                             label='نام مدرسه')
    zone = forms.CharField(widget=forms.TextInput(attrs={'class': 'formbold-form-input', 'placeholder': 'منطقه'}),
                           label='منطقه')
    meli_code = forms.CharField(widget=forms.TextInput(attrs={'class': 'formbold-form-input', 'placeholder': 'کدملی'}),
                                label='کدملی')
    birthday = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'formbold-form-input', 'placeholder': 'تاریخ تولد'}),
        label='تاریخ تولد')


class LoginUserForm(forms.Form):
    phone = forms.CharField(widget=forms.TextInput(attrs={'class': 'formbold-form-input', 'placeholder': ''}),
                            label="موبایل")
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'formbold-form-input', 'placeholder': ''}),
                               label='رمز ورود')
