from django.shortcuts import get_object_or_404, redirect, render, reverse
from make_qrcode.models import QRCode


def router(request, qr_id):
    qr = get_object_or_404(QRCode, unique_id=qr_id)
    if qr.user:
        return redirect(reverse('login-view'))
    return redirect('register-tree', qr_id)


def index(request):
    return render(request, 'index.html', {'title': 'صفحه اصلی'})


def about(request):
    return render(request, 'about.html', {'title': 'درباره ما'})
