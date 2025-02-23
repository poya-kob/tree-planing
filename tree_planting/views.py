from django.shortcuts import redirect, get_object_or_404, render
from make_qrcode.models import QRCode


def router(request, qr_id):
    qr = get_object_or_404(QRCode, unique_id=qr_id)
    if qr.user:
        # todo:redirect to login page
        return 200
    return redirect('register-tree', qr_id)


def index(request):
    return render(request, 'index.html', {'title': 'صفحه اصلی'})
