from PIL import Image, ImageDraw, ImageFont
import qrcode
import os
from django.conf import settings
from django.http import FileResponse
from django.shortcuts import render
from .models import QRCode
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

QR_CODE_DIR = os.path.join(settings.MEDIA_ROOT, 'qrcodes')
os.makedirs(QR_CODE_DIR, exist_ok=True)


def get_persian_font(font_size=40):
    """ تابعی برای یافتن یک فونت مناسب برای متن فارسی """
    possible_fonts = [
        "B Nazanin Bold-tamirpc.net.ttf",
        "B Nazanin.ttf",  # اگر فونت روی سیستم موجود است
        "BNazanin.ttf",
        "Tahoma.ttf",
        "Arial.ttf",
    ]

    for font_name in possible_fonts:
        try:
            font_path = os.path.join("C:\\Windows\\Fonts",
                                     font_name) if os.name == "nt" else f"/usr/share/fonts/{font_name}"
            return ImageFont.truetype(font_path, font_size)
        except:
            continue

    return ImageFont.load_default()


def generate_qrcodes(request):
    if request.method == "POST":
        num_qr = int(request.POST.get('num_qr', 1))  # تعداد QR Code موردنظر

        qr_data = []
        domain = request.get_host()  # دریافت دامنه سایت

        for i in range(1, num_qr + 1):
            qr = QRCode.objects.create()
            qr_link = f"http://nojavaneshahr.ir/{qr.unique_id}/"  # لینک داینامیک

            # تولید QR Code
            qr_img = qrcode.QRCode(
                version=10,
                error_correction=qrcode.constants.ERROR_CORRECT_H,
                box_size=20,
                border=4
            )
            qr_img.add_data(qr_link)
            qr_img.make(fit=True)

            qr_img_pil = qr_img.make_image(fill="black", back_color="white")
            qr_filename = f"{qr.unique_id}.png"
            qr_path = os.path.join(QR_CODE_DIR, qr_filename)
            qr_img_pil.save(qr_path)
            qr.qr_image = f"qrcodes/{qr_filename}"

            qr.save()

            qr_data.append((qr_path, qr_link, i*1000))  # اضافه کردن شماره برای نمایش

        # بارگذاری تمپلیت (qrtemp.jpg)
        template_path = os.path.join(settings.MEDIA_ROOT, 'qrtemp.jpg')  # مسیر فایل تمپلیت شما
        template = Image.open(template_path)

        # مختصات کادر سفید برای شماره QR
        text_x, text_y = 388, 614  # موقعیت متن
        text_color = "#bbf6be"  # رنگ متن

        # استفاده از فونت مناسب
        font = get_persian_font(font_size=40)

        # تولید PDF
        pdf_path = os.path.join(QR_CODE_DIR, "qrcodes.pdf")
        pdf = canvas.Canvas(pdf_path, pagesize=(1024, 1345))

        # اضافه کردن کد QR و شماره به هر تمپلیت
        for qr_path, qr_link, serial_number in qr_data:
            qr_image = Image.open(qr_path).resize((450, 450))  # تغییر اندازه کد QR

            # بارگذاری تصویر تمپلیت
            template = Image.open(template_path)
            draw = ImageDraw.Draw(template)

            # تبدیل عدد به فارسی
            persian_numbers = "۰۱۲۳۴۵۶۷۸۹"
            serial_fa = "".join(persian_numbers[int(digit)] for digit in str(serial_number))

            # اضافه کردن شماره به تصویر
            draw.text((text_x, text_y), serial_fa, font=font, fill=text_color)

            # جایگذاری QR در تمپلیت
            left, top = 285, 672
            template.paste(qr_image, (left, top))
            template.save("temp_template_for_pdf.jpg")

            # اضافه کردن تصویر به PDF
            template_reader = ImageReader("temp_template_for_pdf.jpg")
            pdf.drawImage(template_reader, 0, 0, width=1024, height=1345)

            pdf.showPage()

        pdf.save()

        # ارسال PDF به کاربر
        return FileResponse(open(pdf_path, "rb"), as_attachment=True, filename="qrcodes.pdf")

    return render(request, 'generate_qrcodes.html')
