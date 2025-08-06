from django.db import models
from colorthief import ColorThief
from io import BytesIO
from PIL import Image
from .collection import Collection
import requests

class Carpet(models.Model):
    STYLE_CHOICES = [
        ('modern', 'Modern'),
        ('classic', 'Classic'),
        ('abstraction', 'Abstraction'),
    ]

    PERCENT_CHOICES = [(f"{i}%", f"{i}%") for i in range(0, 101, 5)] + [("-", "-")]
    THREAD_MATERIAL_CHOICES = [
        ('POLYESTER', 'POLYESTER'),
        ('AKRIL', 'AKRIL'),
        ('BCF', 'BCF'),
        ('Polip Heat Set', 'Polip Heat Set'),
        ('-', '-')
    ]
    THREAD_NOTE_CHOICES = [
        ('PP', 'PP'),
        ('-', '-')
    ]

    collection = models.ForeignKey(
        'catalog.Collection',
        on_delete=models.CASCADE,
        related_name='carpets',
        verbose_name="Коллекция"
    )
    name = models.CharField("Название ковра", max_length=100)
    code = models.CharField("Код названия", max_length=100, blank=True, default='')
    color = models.CharField("Цвет", max_length=50)
    image = models.CharField("Изображение (URL)", max_length=500, blank=True, null=True)
    main_colors = models.JSONField(null=True, blank=True)
    style = models.CharField("Стиль", max_length=20, choices=STYLE_CHOICES, default='modern')

    # Технические характеристики
    loom_width = models.CharField("Ширина станка", max_length=50, blank=True)
    quality = models.CharField("Качество", max_length=60, blank=True)
    pile_height = models.CharField("Высота ворса", max_length=30, blank=True)
    weight = models.CharField("Нетто кг/м²", max_length=30, blank=True)

    # Новый состав нитей
    thread_percent_left = models.CharField("Левый %", max_length=4, blank=True)
    thread_material_left = models.CharField("Левый материал", max_length=50, blank=True)
    thread_percent_right = models.CharField("Правый %", max_length=4, blank=True)
    thread_note = models.CharField("Примечание", max_length=10, blank=True)

    def save(self, *args, **kwargs):
        if self.image:
            self.main_colors = get_main_colors(self.image)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.code})"

def get_main_colors(image_url, num_colors=3):
    try:
        resp = requests.get(image_url)
        resp.raise_for_status()
        with BytesIO(resp.content) as buf:
            ct = ColorThief(buf)
            palette = ct.get_palette(color_count=num_colors)
            return [f'#{r:02x}{g:02x}{b:02x}' for r,g,b in palette]
    except:
        return []