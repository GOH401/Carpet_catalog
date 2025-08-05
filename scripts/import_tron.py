import os
import random
from django.conf import settings
from catalog.models import Carpet, Collection

source_dir = os.path.join(settings.MEDIA_ROOT, 'tron')
collection_id = 10

try:
    collection = Collection.objects.get(id=collection_id)
except Collection.DoesNotExist:
    print(f"❌ Коллекция с ID={collection_id} не найдена.")
    exit()

STYLE_CHOICES = ['modern', 'classic', 'abstraction']
MATERIALS = ['Полиэстер', 'Шерсть', 'Хлопок', 'Вискоза', 'Акрил']
DENSITIES = ['1200 г/м²', '1500 г/м²', '1700 г/м²', '2000 г/м²']
HEIGHTS = ['6 мм', '8 мм', '10 мм', '12 мм']
WEIGHTS = ['2.1 кг/м²', '2.5 кг/м²', '2.7 кг/м²', '3.0 кг/м²']
BACKINGS = ['Джут', 'Хлопковая основа', 'Полиэстер']
METHODS = ['Машинное', 'Ткачество', 'Тафтинг']

created = 0
skipped = 0

for filename in os.listdir(source_dir):
    if not filename.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
        continue

    name_no_ext = os.path.splitext(filename)[0]

    if '_' not in name_no_ext:
        print(f"⚠️ Пропущен файл без '_': {filename}")
        skipped += 1
        continue

    code = name_no_ext.split('_')[0]
    color = "_".join(name_no_ext.split('_')[1:])
    image_path = f"carpets/{filename}"

    if Carpet.objects.filter(code=code, color=color, collection=collection).exists():
        print(f"🔁 Уже существует: {filename}")
        skipped += 1
        continue

    Carpet.objects.create(
        collection=collection,
        name=name_no_ext,
        code=code,
        color=color,
        image=image_path,
        style=random.choice(STYLE_CHOICES),
        material=random.choice(MATERIALS),
        density=random.choice(DENSITIES),
        pile_height=random.choice(HEIGHTS),
        weight=random.choice(WEIGHTS),
        backing=random.choice(BACKINGS),
        manufacturing_method=random.choice(METHODS),
    )
    print(f"✅ Добавлен: {name_no_ext}")
    created += 1

print(f"\n🎉 Всего добавлено: {created}, Пропущено: {skipped}")
