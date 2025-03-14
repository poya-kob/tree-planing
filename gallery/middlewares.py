from django.utils.deprecation import MiddlewareMixin
from .models import TreeImage


class RandomGalleryMiddleware(MiddlewareMixin):
    def get_random_images(self):
        """
        تابع برای انتخاب 9 تصویر تصادفی از مدل TreeImage
        """
        return TreeImage.objects.filter(is_active=True).order_by('?')[:9]

    def process_request(self, request):
        request.random_gallery = self.get_random_images()
