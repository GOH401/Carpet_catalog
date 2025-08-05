# scripts/migrate_existing_images.py

import os
import sys
import django

# Добавляем путь к проекту
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "maib.settings")
django.setup()

from django.conf import settings
from django.core.files import File
from maib.catalog.models import Carpet

def migrate_images():
    media_root = settings.MEDIA_ROOT
    success, skipped, failed = 0, 0, 0

    for carpet in Carpet.objects.all():
        if not carpet.image:
            print(f"⛔ Пропущено (нет изображения): {carpet}")
            skipped += 1
            continue

        if 'cloudinary.com' in carpet.image.url:
            print(f"✅ Уже в Cloudinary: {carpet.name}")
            skipped += 1
            continue

        local_path = os.path.join(media_root, carpet.image.name)

        if not os.path.exists(local_path):
            print(f"❌ Файл не найден: {local_path}")
            failed += 1
            continue

        print(f"⏫ Загружается в Cloudinary: {local_path}")
        with open(local_path, 'rb') as f:
            carpet.image.save(os.path.basename(local_path), File(f), save=True)
        print(f"✅ Обновлён: {carpet.name}")
        success += 1

    print("\n--- Результаты миграции ---")
    print(f"Загружено: {success}")
    print(f"Пропущено: {skipped}")
    print(f"Не найдено файлов: {failed}")

if __name__ == "__main__":
    migrate_images()
