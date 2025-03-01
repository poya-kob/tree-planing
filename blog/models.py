# from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from tree_planting.utils import upload_image_path


class Category(models.Model):
    title = models.CharField(max_length=150, verbose_name="عنوان دسته بندی")
    active = models.BooleanField(default=False, verbose_name="فعال/غیرفعال")


class Blog(models.Model):
    title = models.CharField(max_length=150, verbose_name="عنوان مطلب")
    image = models.ImageField(upload_to=upload_image_path, verbose_name="بنر خبر -300*360-")
    active = models.BooleanField(default=False, verbose_name="فعال/غیرفعال")
    date = models.DateTimeField(auto_now_add=True, verbose_name="زمان ایجاد پست")
    description = models.TextField(max_length=690, verbose_name="توضیحات کوتاه(یک پاراگراف)")
    text = models.TextField(verbose_name="متن خبر")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='blogs')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "اخبار"
        verbose_name = "خبر"
