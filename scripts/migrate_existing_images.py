import os
import sys
import django
from pathlib import Path
from dotenv import load_dotenv

# --- 🔧 Настройка путей и окружения ---
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_DIR = SCRIPT_DIR.parent
sys.path.append(str(PROJECT_DIR))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'maib.settings')
load_dotenv(PROJECT_DIR / '.env')

django.setup()

# --- 📦 Импорты Django и Supabase ---
from maib.utils.supabase_client import supabase
from maib.catalog.models import Carpet

# --- 🚀 Загрузка изображений с учётом дубликатов ---
def upload_images_to_supabase():
    success, skipped, failed = 0, 0, 0

    for carpet in Carpet.objects.all():
        try:
            if not carpet.image:
                print(f"⛔ Пропущено (нет изображения): {carpet.name}")
                skipped += 1
                continue

            file_name = f"{carpet.name.replace(' ', '_')}.jpg"
            local_path = os.path.join('media', 'carpets', file_name)
            print(f"🔍 Проверяем локальный файл: {local_path}")

            if not os.path.exists(local_path):
                print(f"❌ Файл не найден: {carpet.name} → {local_path}")
                failed += 1
                continue

            print(f"🔄 Загружаем {file_name} в balcatalog/public/")
            # Попытка загрузки
            try:
                result = supabase.storage.from_("balcatalog").upload(
                    path=f"public/{file_name}",
                    file=open(local_path, "rb")
                )
            except Exception as e:
                err = e.args[0] if e.args else str(e)
                # Если 409 Duplicate – пропускаем как успешную загрузку
                if isinstance(err, dict) and err.get("statusCode") == 409 \
                   or "Duplicate" in str(err):
                    print(f"🔁 Уже есть: {carpet.name}, пропускаем")
                    skipped += 1
                    continue
                else:
                    raise

            print("📥 Ответ Supabase:", result)

            public_url = (
                f"{os.getenv('SUPABASE_URL')}"
                f"/storage/v1/object/public/balcatalog/public/{file_name}"
            )
            Carpet.objects.filter(pk=carpet.pk).update(image=public_url)
            print(f"✅ Загружено: {carpet.name} → {public_url}")
            success += 1

        except Exception as e:
            print(f"💥 Ошибка: {carpet.name} → {e}")
            failed += 1

    print("\n📊 Результат миграции:")
    print(f"✅ Успешно: {success}")
    print(f"🔁 Пропущено (уже или нет image): {skipped}")
    print(f"❌ Ошибок: {failed}")


if __name__ == "__main__":
    upload_images_to_supabase()
