from django_ckeditor_5.fields import CKEditor5Field
from django.db import models
from tree_planting.utils import upload_image_path


class Category(models.Model):
    title = models.CharField(max_length=150, verbose_name="عنوان دسته بندی")
    active = models.BooleanField(default=False, verbose_name="فعال/غیرفعال")

    def __str__(self):
        return self.title


class Blog(models.Model):
    title = models.CharField(max_length=150, verbose_name="عنوان مطلب")
    image = models.ImageField(upload_to=upload_image_path, verbose_name="بنر خبر -300*360-")
    active = models.BooleanField(default=False, verbose_name="فعال/غیرفعال")
    date = models.DateTimeField(auto_now_add=True, verbose_name="زمان ایجاد پست")
    description = models.TextField(max_length=690, verbose_name="توضیحات کوتاه(یک پاراگراف)")
    text = CKEditor5Field(verbose_name="متن خبر", config_name='default')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='blogs')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "اخبار"
        verbose_name = "خبر"


class Comment(models.Model):
    name = models.CharField(max_length=100, verbose_name="نام کاربر")
    email = models.EmailField(verbose_name="ایمیل کاربر")
    text = models.TextField(verbose_name="متن نظر")
    date = models.DateTimeField(auto_now_add=True, verbose_name="زمان ارسال نظر")
    is_active = models.BooleanField(default=False, verbose_name="تایید شده")

    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='comments', verbose_name="بلاگ مربوطه")

    admin_reply = models.TextField(blank=True, null=True, verbose_name="پاسخ ادمین")
    reply_date = models.DateTimeField(blank=True, null=True, verbose_name="زمان پاسخ ادمین")

    def __str__(self):
        return f"نظر {self.name} برای {self.blog}"

    class Meta:
        verbose_name = "نظر"
        verbose_name_plural = "نظرات"
