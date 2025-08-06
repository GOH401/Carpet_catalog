import io
from django.core.serializers import serialize
from maib.catalog.models import Carpet

with io.open("carpets.json", "w", encoding="utf-8") as f:
    data = serialize("json", Carpet.objects.all(), indent=2)
    f.write(data)
