import os
import shutil
from django.conf import settings


def move_qr_to_user_folder(user, qr_code_path):
    """
    انتقال QR Code به پوشه‌ی اختصاصی کاربر
    """
    user_folder = os.path.join(settings.MEDIA_ROOT, "users", user.phone)

    if not os.path.exists(user_folder):
        os.makedirs(user_folder)

    qr_filename = os.path.basename(qr_code_path)  # نام فایل QR Code
    new_qr_path = os.path.join(user_folder, qr_filename)

    shutil.move(qr_code_path, new_qr_path)

    return new_qr_path  # مسیر جدید فایل را برمی‌گرداند
