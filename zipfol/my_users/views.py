from django.shortcuts import render, get_object_or_404, HttpResponse, redirect
from django.contrib.auth import login, authenticate, get_user_model
from .forms import UsersFrom
from make_qrcode.models import QRCode
from tree_planting.utils import move_qr_to_user_folder

MyUsers = get_user_model()


def register_tree(request, qr_id):
    qr = get_object_or_404(QRCode, unique_id=qr_id)
    if qr.user:
        return HttpResponse('این درخت به نام کاربر دیگری ثبت شده است')
    user_form = UsersFrom(request.POST or None)
    if request.POST:
        if user_form.is_valid():
            phone = user_form.cleaned_data.get('phone')
            if MyUsers.objects.filter(phone=phone).exists():
                user = MyUsers.objects.get(phone=phone)
            else:
                first_name = user_form.cleaned_data.get('first_name')
                last_name = user_form.cleaned_data.get('last_name')
                user = MyUsers.objects.create_user(phone, first_name, last_name)
                qr.user = user
                qr.save()
            login(request, user, backend='my_users.auth_backend.PhoneAuthBackend')
            move_qr_to_user_folder(user, qr.qr_image.path)
            qr.qr_image = f'users/{user.phone}/{qr.unique_id}.png'
            qr.user = user
            qr.save()
            return redirect('dashboard')
        else:
            return render(request, 'register_tree.html', {'form': user_form, 'error': "شماره موبایل صحیح نیست."})

    return render(request, 'register_tree.html', {'form': user_form, 'qr': qr})


def login_view(request):
    if request.user.is_anonymous:
        return redirect("dashboard")
    if request.method == "POST":
        phone = request.POST.get("phone")
        user = MyUsers.objects.filter(phone=phone)

        if user:
            login(request, user[0], backend='my_users.auth_backend.PhoneAuthBackend')  # لاگین بدون پسورد
            return redirect("dashboard")
        else:
            return render(request, "login.html", {"error": "شماره موبایل یافت نشد!"})

    return render(request, "login.html")
