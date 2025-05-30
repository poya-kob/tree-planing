from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


class CustomUserManager(BaseUserManager):
    def create_user(self, phone, *arg, **kwargs):
        """ ایجاد یوزر عادی بدون نیاز به پسورد """
        if not phone:
            raise ValueError("شماره موبایل الزامی است")

        user = self.model(phone=phone, **kwargs)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password, **extra_fields):
        """ ایجاد سوپریوزر که نیاز به پسورد دارد """
        if not phone:
            raise ValueError("شماره موبایل الزامی است")
        if not password:
            raise ValueError("پسورد الزامی است برای سوپریوزر")

        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        # مقدار birthday را اضافه کنید
        extra_fields.setdefault("birthday", "2000-01-01")  # مقدار پیش‌فرض

        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)  # ست کردن پسورد فقط برای سوپریوزر
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    phone = models.CharField(max_length=11, unique=True)  # شماره موبایل یکتا
    meli_code = models.CharField(max_length=10, unique=True)  # کدملی یکتا
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    birthday = models.DateField()
    stage = models.CharField(max_length=255, blank=True, null=True)  # مقطع تحصیلی
    school = models.CharField(max_length=255, blank=True, null=True)  # نام مدرسه
    zone = models.CharField(max_length=255, blank=True, null=True)  # منطقه
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = "phone"  # شماره موبایل به عنوان نام کاربری
    REQUIRED_FIELDS = []  # برای یوزر معمولی هیچ فیلد اجباری دیگری وجود ندارد

    def __str__(self):
        return self.phone

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'


class ContactUs(models.Model):
    subject = models.CharField(max_length=200)
    name = models.CharField(max_length=50, null=True, blank=True)
    phone = models.CharField(max_length=11)
    email = models.EmailField()
    massage = models.TextField()
