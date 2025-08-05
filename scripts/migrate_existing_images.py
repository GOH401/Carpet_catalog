import os
import sys
import django

# 👇 Добавляем путь к корню проекта (где manage.py)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

# ⚙️ Установка settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "maib.settings")

# 🧠 Django setup
django.setup()

# ✅ Импорты после setup
from django.conf import settings
from django.core.files import File
from maib.catalog.models import Carpet

def migrate_images():
    media_root = settings.MEDIA_ROOT

    for carpet in Carpet.objects.all():
        if not carpet.image:
            print(f"⛔ Пропущено (нет изображения): {carpet}")
            continue

        if 'cloudinary.com' in carpet.image.url:
            print(f"✅ Уже в Cloudinary: {carpet.name}")
            continue

        local_path = os.path.join(media_root, carpet.image.name)

        if not os.path.exists(local_path):
            print(f"❌ Файл не найден: {local_path}")
            continue

        print(f"⏫ Загружается в Cloudinary: {local_path}")
        with open(local_path, 'rb') as f:
            carpet.image.save(os.path.basename(local_path), File(f), save=True)

        print(f"✅ Обновлён: {carpet.name}")

if __name__ == "__main__":
    migrate_images()
