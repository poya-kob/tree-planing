import qrcode
import os
from django.conf import settings
from django.http import FileResponse
from django.shortcuts import render
from .models import QRCode
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from django.core.files import File  # you need this somewhere

QR_CODE_DIR = os.path.join(settings.MEDIA_ROOT, 'qrcodes')
os.makedirs(QR_CODE_DIR, exist_ok=True)


def generate_qrcodes(request):
    if request.method == "POST":
        num_qr = int(request.POST.get('num_qr', 1))  # تعداد QR Code موردنظر

        qr_data = []
        domain = request.get_host()  # دریافت دامنه سایت

        for _ in range(num_qr):
            qr = QRCode.objects.create()
            qr_link = f"http://{domain}/{qr.unique_id}/"  # لینک داینامیک

            # تولید QR Code
            qr_img = qrcode.QRCode(
                version=10,  # سایز
                error_correction=qrcode.constants.ERROR_CORRECT_H,  # سطح تصحیح خطا
                box_size=20,  # ابعاد هر سلول QR
                border=4  # مقدار استاندارد حاشیه
            )
            qr_img.add_data(qr_link)
            qr_img.make(fit=True)

            qr_img_pil = qr_img.make_image(fill="black", back_color="white")
            qr_filename = f"{qr.unique_id}.png"
            qr_path = os.path.join(QR_CODE_DIR, qr_filename)
            qr_img_pil.save(qr_path)
            qr.qr_image = f"qrcodes/{qr_filename}"

            qr.save()

            qr_data.append((qr_path, qr_link))  # ذخیره مسیر فایل برای PDF

        # تولید PDF
        pdf_path = os.path.join(QR_CODE_DIR, "qrcodes.pdf")
        pdf = canvas.Canvas(pdf_path)

        for qr_path, qr_link in qr_data:
            # بارگذاری تصویر QR Code
            qr_image = ImageReader(qr_path)

            # تنظیم اندازه تصویر QR Code
            qr_size = 400  # افزایش سایز QR Code

            # تنظیم عرض و ارتفاع صفحه متناسب با محتوا
            link_width = pdf.stringWidth(qr_link, "Helvetica", 16) + 40  # عرض لینک + حاشیه
            page_width = max(qr_size + 100, link_width)  # عرض صفحه متناسب با متن لینک
            page_height = qr_size + 100  # ارتفاع متناسب

            pdf.setPageSize((page_width, page_height))

            # اضافه کردن QR Code به وسط صفحه
            x = (page_width - qr_size) / 2
            y = (page_height - qr_size - 40)  # کمی بالاتر از پایین صفحه
            pdf.drawImage(qr_image, x, y, width=qr_size, height=qr_size)

            # اضافه کردن لینک زیر QR Code
            pdf.setFont("Helvetica", 16)
            text_x = (page_width - pdf.stringWidth(qr_link, "Helvetica", 16)) / 2
            pdf.drawString(text_x, 20, qr_link)

            pdf.showPage()  # ایجاد صفحه جدید برای QR Code بعدی

        pdf.save()

        return FileResponse(open(pdf_path, "rb"), as_attachment=True, filename="qrcodes.pdf")

    return render(request, 'generate_qrcodes.html')
