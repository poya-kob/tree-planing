from django.shortcuts import render, get_object_or_404
from .models import Blog


def blog_list(request):
    blogs = Blog.objects.filter(active=True)
    return render(request, 'blog_list.html', {'title': 'لیست مطالب',
                                              'blogs': blogs})


def blog_detail(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    return render(request, 'blog_list.html', {'title': 'مطلب',
                                              'blog': blog})
