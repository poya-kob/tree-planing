from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView

from .models import Blog, Category
from .forms import BlogForm, CommentForm


def create_blog(request):
    if request.method == "POST":
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save()
            if request.user.is_superuser:
                post.active = True
                post.save()
            # return redirect("home")  # تغییر مسیر بعد از ارسال موفق
    else:
        form = BlogForm()

    return render(request, "dashboard/create_blog_post.html", {"form": form})


class BlogListView(ListView):
    model = Blog
    template_name = 'blog_list.html'
    context_object_name = 'blogs'
    extra_context = {'title': 'مطالب'}
    paginate_by = 9

    def get_queryset(self):
        return Blog.objects.filter(active=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class BlogDetailView(DetailView):
    model = Blog
    template_name = 'blog_detail.html'
    context_object_name = 'blog'
    extra_context = {'title': 'مطلب'}

    def get_object(self, queryset=None):
        return get_object_or_404(Blog, id=self.kwargs.get('pk'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        context['comments'] = self.object.comments.filter(is_active=True)
        context['next'] = self.model.objects.filter(active=True).filter(date__gt=self.object.date).first()
        context['previous'] = self.model.objects.filter(active=True).filter(date__lt=self.object.date).first()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.blog = self.object
            comment.save()
            return redirect('blogs-detail', pk=self.object.pk)  # بعد از ارسال، صفحه دوباره لود شود
        return self.get(request, *args, **kwargs)  # اگر فرم نامعتبر بود، صفحه با ارور نمایش داده شود
