# maib/catalog/models.py
from django.db import models
from django.conf import settings

class Collection(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    main_colors = models.CharField(max_length=255, blank=True, verbose_name="Основные цвета (через запятую)")
    image_url = models.URLField(blank=True, null=True, verbose_name="Изображение превью (публичный URL)")

    def __str__(self):
        return self.name

    def get_main_colors_list(self):
        return [c.strip() for c in self.main_colors.split(',') if c.strip()]

    def get_image_url(self):
        # 1) Явно заданный URL
        if self.image_url and self.image_url.strip():
            return self.image_url.strip()

        # 2) Фото из первого ковра (поддержим и carpets, и carpet_set)
        rel = None
        if hasattr(self, 'carpets'):
            rel = self.carpets
        elif hasattr(self, 'carpet_set'):
            rel = self.carpet_set

        if rel:
            first = rel.first()
            if first:
                getter = getattr(first, 'get_image_url', None)
                if callable(getter):
                    return getter()
                img = getattr(first, 'image', None)
                if img and getattr(img, 'url', None):
                    return img.url

        # 3) Плейсхолдер из static
        return settings.STATIC_URL + 'img/collection_placeholder.jpg'
