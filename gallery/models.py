from django.db import models
from tree_planting.utils import upload_image_path
from make_qrcode.models import QRCode


class TreeImage(models.Model):
    title = models.CharField(max_length=150, verbose_name="عنوان تصویر")
    image = models.ImageField(upload_to=upload_image_path, verbose_name='تصویر درخت')
    tree = models.ForeignKey(QRCode, on_delete=models.CASCADE, related_name='images', verbose_name="انتخاب درخت")

    class Meta:
        verbose_name_plural = 'تصویر'
        verbose_name = 'تصویر'

    def __str__(self):
        return self.title
