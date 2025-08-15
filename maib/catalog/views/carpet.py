from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from maib.catalog.models import Carpet
from maib.catalog.forms import CarpetForm
from maib.catalog.supabase_client import upload_public
from pathlib import Path
from django.conf import settings
from django.views.decorators.http import require_http_methods

def _norm(s: str) -> str:
    return (s or "").strip().replace(" ", "_").replace("/", "_").upper()

def _make_key(code: str, color: str, ext: str) -> str:
    return f"{settings.SUPABASE_FOLDER}/{_norm(code)}_{_norm(color)}{(ext or '.jpg').lower()}"

@login_required
def carpet_create(request):
    if request.method == 'POST':
        form = CarpetForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            f = form.cleaned_data.get('upload')
            if f:  # файл имеет приоритет над ручным URL
                key = _make_key(obj.code, obj.color, Path(f.name).suffix)
                obj.image = upload_public(f.read(), getattr(f, 'content_type', 'image/jpeg'), key)
            obj.save()
            messages.success(request, 'Товар добавлен')
            return redirect('collection_detail', pk=obj.collection_id)
    else:
        form = CarpetForm()
    return render(request, 'catalog/catalog_form.html', {'form': form})

@login_required
def carpet_update(request, pk):
    obj = get_object_or_404(Carpet, pk=pk)
    if request.method == 'POST':
        form = CarpetForm(request.POST, request.FILES, instance=obj)
        if form.is_valid():
            obj = form.save(commit=False)
            f = form.cleaned_data.get('upload')
            if f:
                key = _make_key(obj.code, obj.color, Path(f.name).suffix)
                obj.image = upload_public(f.read(), getattr(f, 'content_type', 'image/jpeg'), key)
            obj.save()
            messages.success(request, 'Изменения сохранены')
            return redirect('collection_detail', pk=obj.collection_id)
    else:
        form = CarpetForm(instance=obj)
    return render(request, 'catalog/catalog_form.html', {'form': form, 'carpet': obj})


@login_required
@require_http_methods(["GET", "POST"])
def carpet_delete(request, pk):
    carpet = Carpet.objects.filter(pk=pk).select_related('collection').first()
    if not carpet:
        messages.info(request, "Ковер уже удалён или не найден.")
        return redirect('collection_cards')   # или на нужную страницу

    if request.method == "POST":
        collection_id = carpet.collection_id
        carpet.delete()
        messages.success(request, "Ковер удалён.")
        return redirect('collection_detail', pk=collection_id)

    # GET: показать подтверждение
    return render(request, "catalog/catalog_confirm_delete.html", {"carpet": carpet})