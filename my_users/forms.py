from django import forms
from django.core.exceptions import ValidationError
import re
import datetime


def validate_phone(value):
    """ بررسی شماره موبایل که باید ۱۱ رقمی باشد و با 09 شروع شود. """
    if not re.fullmatch(r'09\d{9}', value):
        raise ValidationError("شماره موبایل باید ۱۱ رقمی و با 09 شروع شود.")


def validate_meli_code(value):
    """ بررسی صحت کد ملی (۱۰ رقم عددی) و الگوریتم بررسی کد ملی ایران """
    if not re.fullmatch(r'\d{10}', value):
        raise ValidationError("کد ملی باید ۱۰ رقم باشد.")

    # الگوریتم بررسی صحت کد ملی ایران
    check = int(value[9])
    s = sum(int(value[i]) * (10 - i) for i in range(9)) % 11
    if not ((s < 2 and check == s) or (s >= 2 and check + s == 11)):
        raise ValidationError("کد ملی وارد شده معتبر نیست.")


def validate_name(value):
    """ بررسی اینکه نام و نام خانوادگی فقط شامل حروف فارسی باشد. """
    if not re.fullmatch(r'^[آ-ی\s]+$', value):
        raise ValidationError("نام فقط می‌تواند شامل حروف فارسی باشد.")


def validate_zone(value):
    """ بررسی اینکه مقدار منطقه فقط شامل اعداد باشد. """
    if not value.isdigit():
        raise ValidationError("منطقه باید فقط شامل اعداد باشد.")


def validate_birthday(value):
    """ بررسی اینکه تاریخ تولد نباید در آینده باشد. """
    if value > datetime.date.today():
        raise ValidationError("تاریخ تولد نمی‌تواند در آینده باشد.")


class UsersFrom(forms.Form):
    phone = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': ' شماره موبایل'}),
        label="شماره موبایل",
        validators=[validate_phone]
    )
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': ' نام'}),
        label="نام",
        validators=[validate_name]
    )
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': ' نام خانوادگی'}),
        label="نام خانوادگی",
        validators=[validate_name]
    )
    stage = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': ' مقطع تحصیلی'}),
        label="مقطع تحصیلی"
    )
    school = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': ' نام مدرسه'}),
        label="نام مدرسه"
    )
    zone = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': ' منطقه'}),
        label="منطقه",
        validators=[validate_zone]
    )
    meli_code = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': ' کد ملی'}),
        label="کد ملی",
        validators=[validate_meli_code]
    )
    birthday = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        label="تاریخ تولد",
        validators=[validate_birthday]
    )


class LoginUserForm(forms.Form):
    phone = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'مثلاً: 09123456789'}),
        label="شماره موبایل",
        validators=[validate_phone]
    )
    meli_code = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'مثلاً: 1234567890'}),
        label="کد ملی",
        validators=[validate_meli_code]
    )


class ContactForm(forms.Form):
    name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'مثلاً: علی'}),
        label="نام",
        validators=[validate_name]
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'مثلاً: example@email.com'}),
        label="ایمیل"
    )
    phone = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'مثلاً: 09123456789'}),
        label="شماره تلفن",
        validators=[validate_phone],
        required=False  # چون ممکن است کاربر تلفن را وارد نکند
    )
    subject = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'مثلاً: درخواست همکاری'}),
        label="موضوع"
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'پیام شما'}),
        label="پیام"
    )
