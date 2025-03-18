from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, View, DetailView
from django.shortcuts import redirect
from django.contrib import messages

from make_qrcode.models import QRCode
from gallery.models import TreeImage
from .forms import TreeImageUploadForm


class UnapprovedImagesView(ListView):
    model = TreeImage
    template_name = "./dashboard/admin_image_list.html"
    context_object_name = "images"
    paginate_by = 9  # تعداد عکس‌ها در هر صفحه

    def get_queryset(self):
        return self.model.objects.filter(is_active=False)


class ApproveImagesView(View):
    def post(self, request, *args, **kwargs):
        approved_image_ids = request.POST.getlist("approved_images")
        if not approved_image_ids:
            messages.warning(request, "هیچ تصویری برای تأیید انتخاب نشده است.")
            return redirect("unapproved-images")
        images_updated = TreeImage.objects.filter(id__in=approved_image_ids, is_active=False).update(is_active=True)
        messages.success(request, f"{images_updated} تصویر تأیید شد.")
        return redirect("unapproved-images")


class TreeListView(ListView):
    model = QRCode
    template_name = "./dashboard/trees_list.html"
    context_object_name = "trees"
    paginate_by = 9  # تعداد آیتم‌ها در هر صفحه

    def get_queryset(self):
        if not self.request.user.is_superuser:
            return self.request.user.trees.all()
        queryset = self.model.objects.all()
        status = self.request.GET.get("status")
        if status == "registered":
            queryset = queryset.filter(is_registered=True)
        elif status == "unregistered":
            queryset = queryset.filter(is_registered=False)
        return queryset


class TreeDetailView(DetailView):
    model = QRCode
    template_name = "./dashboard/tree_detail.html"
    context_object_name = "tree"
    slug_field = "unique_id"  # فیلد جایگزین برای جستجو
    slug_url_kwarg = "unique_id"  # مقدار دریافت شده از URL

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = TreeImageUploadForm()
        return context

    def post(self, request, *args, **kwargs):
        tree = self.get_object()
        form = TreeImageUploadForm(request.POST, request.FILES)

        if form.is_valid():
            image = form.save(commit=False)
            image.tree = tree
            image.save()
            messages.success(request, "تصویر جدید با موفقیت اضافه شد.")
        else:
            messages.error(request, "لطفاً یک تصویر معتبر انتخاب کنید.")

        return redirect("tree-detail", unique_id=tree.unique_id)


@login_required
def user_dashboard(request):
    active_trees = QRCode.objects.filter(is_registered=True).count()
    trees_pic = TreeImage.objects.all().count()
    context = {'active_trees': active_trees, 'trees_pic': trees_pic}
    return render(request, './dashboard/user-dashboard.html', context)
