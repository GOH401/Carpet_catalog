from supabase import create_client
from django.conf import settings

_client = create_client(settings.SUPABASE_URL, settings.SUPABASE_SERVICE_ROLE_KEY)

def upload_public(bytes_data: bytes, content_type: str, object_key: str) -> str:
    # object_key: например "public/F053D_BLUE_BLUE.jpg"
    bucket = settings.SUPABASE_BUCKET
    _client.storage.from_(bucket).upload(
        object_key, bytes_data,
        {"content-type": content_type or "image/jpeg", "x-upsert": "true"}
    )
    return f"{settings.SUPABASE_URL}/storage/v1/object/public/{bucket}/{object_key}"
