from django import forms


class UsersFrom(forms.Form):
    phone = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control form-control-lg'}), label="موبایل")
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control form-control-lg'}), label="نام")
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control form-control-lg'}),
                                label="نام خانوادگی")
    stage = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control form-control-lg'}),
                            label='مقطع تحصیلی')
    school = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control form-control-lg'}), label='نام مدرسه')
    zone = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control form-control-lg'}), label='منطقه')
    meli_code = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control form-control-lg'}), label='کدملی')
    birthday = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control form-control-lg'}),
                               label='تاریخ تولد')


class LoginUserForm(forms.Form):
    phone = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control form-control-lg'}), label="موبایل")
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control form-control-lg'}),
                               label='رمز ورود')
