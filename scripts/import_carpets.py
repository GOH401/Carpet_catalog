import os
import random
from django.core.files import File
from maib.catalog.models import Carpet, Collection

# Папка с изображениями ковров (относительно BASE_DIR)
IMAGE_DIR = 'maib/media/arvina'

# Целевая коллекция — обнови ID при необходимости
collection = Collection.objects.get(id=4)

# Справочники
STYLE_CHOICES = ['modern', 'classic', 'abstraction']
PILE_HEIGHT_CHOICES = ['4 мм', '6 мм', '8 мм', '10 мм']
NETTO_CHOICES = ['2 кг/м²', '2.5 кг/м²', '3 кг/м²']
LOOM_WIDTH_CHOICES = ['4 м', '5 м']
PERCENT_VALUES = [f"{i}%" for i in range(0, 101, 5)]
MATERIAL_CHOICES = ['POLYESTER', 'AKRIL', 'BCF', 'Polip Heat Set', '-']
NOTE_CHOICES = ['PP', '-']

# Загрузка ковров
for filename in os.listdir(IMAGE_DIR):
    if not filename.lower().endswith(('.jpg', '.jpeg', '.png')):
        continue

    filepath = os.path.join(IMAGE_DIR, filename)
    name_part = filename.rsplit('.', 1)[0]

    try:
        code, color = name_part.split('_', 1)
    except ValueError:
        print(f"⚠️ Пропущено (неверный формат имени): {filename}")
        continue

    carpet = Carpet(
        collection=collection,
        name=name_part.replace('_', ' '),
        code=code,
        color=color,
        style=random.choice(STYLE_CHOICES),
        loom_width=random.choice(LOOM_WIDTH_CHOICES),
        quality=f"{random.randint(40, 100)}x{random.randint(40, 100)}",
        pile_height=random.choice(PILE_HEIGHT_CHOICES),
        weight=random.choice(NETTO_CHOICES),
        thread_percent_left=random.choice(PERCENT_VALUES),
        thread_material_left=random.choice(MATERIAL_CHOICES),
        thread_percent_right=random.choice(PERCENT_VALUES),
        thread_note=random.choice(NOTE_CHOICES)
    )

    with open(filepath, 'rb') as f:
        carpet.image.save(filename, File(f), save=False)

    carpet.save()
    print(f"✅ Добавлен: {carpet.name}")
