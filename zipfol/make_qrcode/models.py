from django.db import models
from django.contrib.auth import get_user_model
import uuid

MyUsers = get_user_model()


class QRCode(models.Model):
    unique_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    qr_image = models.ImageField(null=True, blank=True)
    user = models.ForeignKey(MyUsers, on_delete=models.DO_NOTHING, null=True, blank=True, related_name='trees')
    is_registered = models.BooleanField(default=False)

    def __str__(self):
        if self.user:
            return f"QR Code {self.user.get_full_name()} - {self.unique_id}"
        return f"QR Code UNKNOWN - {self.unique_id}"
