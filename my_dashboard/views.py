from django.shortcuts import render, get_object_or_404, Http404
from django.contrib.auth.decorators import login_required

from make_qrcode.models import QRCode


@login_required
def user_dashboard(request):
    return render(request, 'user-dashboard.html')


@login_required
def tree_list(request):
    if request.user.is_superuser:
        trees = QRCode.objects.all()
    else:
        trees = request.user.trees.all()
    print(request.user.phone)
    print(trees)
    return render(request, 'trees_list.html', {'trees': trees})


@login_required
def tree_detail(request, qr_id):
    tree = get_object_or_404(QRCode, unique_id=qr_id)
    if not request.user.is_superuser:
        if not tree.user.phone == request.user.phone:
            raise Http404
    return render(request, 'tree_detail.html', {'tree': tree})

