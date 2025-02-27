import os
import string
import random
import datetime
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


def get_file_name(filepath):
    size = 8
    chars = string.ascii_uppercase + string.digits
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    name = ''.join(random.choice(chars) for _ in range(size))

    # print(name)
    return name, ext


def upload_image_path(instance, filename):
    # print(type(instance).__name__)
    date = datetime.datetime.now()
    name, ext = get_file_name(filename)
    new_name = f"{name}{ext}"
    return f"{type(instance).__name__}/{date.year}/{date.month}/{date.day}/{new_name}"
