from django.shortcuts import render, get_object_or_404, HttpResponse, redirect
from django.contrib.auth import login, get_user_model, logout
from django.db.models import Q
from .forms import UsersFrom, LoginUserForm, ContactForm
from make_qrcode.models import QRCode
from tree_planting.utils import move_qr_to_user_folder
from .models import ContactUs
from gallery.models import TreeImage

MyUsers = get_user_model()


# def register(request):
#     user_form = UsersFrom(request.POST or None)
#     return render(request, 'register_tree.html', {'form': user_form})


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
                stage = user_form.cleaned_data.get('stage')
                school = user_form.cleaned_data.get('school')
                zone = user_form.cleaned_data.get('zone')
                meli_code = user_form.cleaned_data.get('meli_code')
                birthday = user_form.cleaned_data.get('birthday')
                phone = user_form.cleaned_data.get('phone')
                user = MyUsers.objects.create_user(phone, first_name, last_name, stage=stage, meli_code=meli_code,
                                                   school=school, zone=zone, birthday=birthday)
                qr.user = user
                qr.is_registered = True
                qr.save()
            if request.FILES['upload']:
                TreeImage.objects.create(title='first-image', image=request.FILES['upload'], tree=qr)

            login(request, user, backend='my_users.auth_backend.PhoneAuthBackend')
            move_qr_to_user_folder(user, qr.qr_image.path)
            qr.qr_image = f'users/{user.phone}/{qr.unique_id}.png'
            qr.user = user
            qr.save()
            return redirect('dashboard')
        else:
            return render(request, 'register_tree.html',
                          {'form': user_form, 'qr': qr, 'error': "شماره موبایل صحیح نیست."})

    return render(request, 'register_tree.html', {'form': user_form, 'qr': qr})


def login_view(request):
    if not request.user.is_anonymous:
        return redirect("dashboard")
    login_form = LoginUserForm(request.POST or None)
    if request.method == "POST":
        phone = request.POST.get("phone")
        meli_code = request.POST.get("meli_code")
        user = MyUsers.objects.filter(Q(phone=phone) & Q(meli_code=meli_code))
        if user:
            login(request, user[0], backend='my_users.auth_backend.PhoneAuthBackend')  # لاگین بدون پسورد
            return redirect("dashboard")
        else:
            return render(request, "login.html", {"error": "اطلاعات اشتباه است!", 'form': login_form})

    return render(request, "login.html", {'form': login_form})


def contact(request):
    message = ""
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = request.POST.get('subject')
            name = request.path.get('name')
            phone = request.path.get('phone')
            email = request.path.get('email')
            message = request.path.get('message')
            ContactUs.objects.create(subject=subject, name=name, phone=phone, email=email, message=message)
            message = "پیام شما با موفقیت ارسال شد."
            form = ContactForm()  # فرم را خالی کن
        else:
            message = "لطفاً خطاهای زیر را برطرف کنید."

    else:
        form = ContactForm()

    return render(request, 'contact.html', {'title': 'تماس با ما', 'form': form, 'message': message})


def logout_page(request):
    logout(request)
    return redirect('index')
