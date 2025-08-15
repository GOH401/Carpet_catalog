from django.core.management.base import BaseCommand
from django.conf import settings
from django.db import transaction
from django.db.models import Q            # <-- добавили
from maib.catalog.models import Carpet    # <-- правильный импорт

def build_name(code: str, color: str) -> str:
    # F053D_BLUE_BLUE → верхний регистр, пробелы/слэши → "_"
    def norm(s):
        return (s or "").strip().replace(" ", "_").replace("/", "_").upper()
    return f"{norm(code)}_{norm(color)}.jpg"

class Command(BaseCommand):
    help = "Fill Carpet.image from SUPABASE_PUBLIC_BASE using <CODE>_<COLOR>.jpg"

    def handle(self, *args, **opts):
        base = getattr(settings, "SUPABASE_PUBLIC_BASE", "").rstrip("/")
        if not base:
            self.stderr.write("SUPABASE_PUBLIC_BASE not set in settings.")
            return

        qs = (Carpet.objects
              .filter(Q(image__isnull=True) | Q(image=""))   # <-- Q вместо models.Q
              .only("id", "code", "color"))

        updated, batch, B = 0, [], 300
        for c in qs.iterator(chunk_size=B):
            c.image = f"{base}/{build_name(c.code, c.color)}"
            batch.append(c)
            if len(batch) >= B:
                with transaction.atomic():
                    Carpet.objects.bulk_update(batch, ["image"])
                updated += len(batch)
                batch.clear()

        if batch:
            with transaction.atomic():
                Carpet.objects.bulk_update(batch, ["image"])
            updated += len(batch)

        self.stdout.write(self.style.SUCCESS(f"Обновлено: {updated}"))
