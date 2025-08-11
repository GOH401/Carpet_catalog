from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from maib.catalog.models import Carpet, Collection
from django.core.paginator import Paginator
from django.db.models import Count, Min, Max

def carpet_list(request, pk = None):
    """Отображение колекции"""
    query = request.GET.get('q', '')
    color = request.GET.get('color', '')
    collection_id = request.GET.get('collection', '')
    style = request.GET.get('style', '')  # Новый фильтр

    collection_id = pk or request.GET.get('collection', '')
    carpets = Carpet.objects.all()

    if query:
        carpets = carpets.filter(
            Q(name__icontains=query) |
            Q(collection__name__icontains=query)
        )

    if color:
        carpets = carpets.filter(color__iexact=color)

    if collection_id:
        carpets = carpets.filter(collection_id=collection_id)

    if style:
        carpets = carpets.filter(style__iexact=style)

    # Уникальные значения для фильтров
    all_colors = Carpet.objects.order_by('color').values_list('color', flat=True).distinct()
    all_collections = Collection.objects.all()
    all_styles = Carpet.objects.order_by('style').values_list('style', flat=True).distinct()

    # Пагинация
    paginator = Paginator(carpets, 12)  # 12 ковров на страницу
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'query': query,
        'color': color,
        'collection': collection_id,
        'style': style,
        'all_colors': all_colors,
        'all_collections': all_collections,
        'all_styles': all_styles,
    }

    return render(request, 'catalog/catalog_list.html', context)

def carpet_detail(request, pk):
    carpet = get_object_or_404(Carpet, pk=pk)

    # Похожие ковры (оставляем как было)
    similar_carpets = Carpet.objects.filter(
        Q(collection=carpet.collection) |
        Q(color__iexact=carpet.color) |
        Q(name__icontains=carpet.name.split('_')[0])
    ).exclude(pk=carpet.pk).distinct()[:6]

    # Навигация по коллекции
    collection_carpets = Carpet.objects.filter(collection=carpet.collection).order_by('id')
    ids = list(collection_carpets.values_list('id', flat=True))
    current_index = ids.index(carpet.id)

    prev_id = ids[current_index - 1] if current_index > 0 else None
    next_id = ids[current_index + 1] if current_index < len(ids) - 1 else None

    context = {
        'carpet': carpet,
        'similar_carpets': similar_carpets,
        'prev_id': prev_id,
        'next_id': next_id,
    }
    return render(request, 'catalog/catalog_detail.html', context)

def collection_cards(request):
    fields = {f.name for f in Collection._meta.get_fields()}
    age_field = 'created_at' if 'created_at' in fields else 'id'

    qs = (Collection.objects
          .only('id', 'name', 'image_url')
          .annotate(carpets_count=Count('carpets', distinct=True))
          .prefetch_related('carpets'))

    q = (request.GET.get('q') or '').strip()
    if q:
        qs = qs.filter(name__icontains=q)

    min_count = request.GET.get('min_count')
    max_count = request.GET.get('max_count')
    if min_count:
        qs = qs.filter(carpets_count__gte=min_count)
    if max_count:
        qs = qs.filter(carpets_count__lte=max_count)

    sort = request.GET.get('sort', 'name_asc')
    order_map = {
        'name_asc': 'name', 'name_desc': '-name',
        'count_desc': '-carpets_count', 'count_asc': 'carpets_count',
        'age_new': f'-{age_field}', 'age_old': f'{age_field}',
    }
    qs = qs.order_by(order_map.get(sort, 'name'))

    stats = (Collection.objects
             .annotate(carpets_count=Count('carpets', distinct=True))
             .aggregate(min_count=Min('carpets_count'), max_count=Max('carpets_count')))

    ctx = {
        'collection_cards': qs,
        'stats': stats,
        'current': {'q': q, 'min_count': min_count or '', 'max_count': max_count or '', 'sort': sort}
    }
    return render(request, 'catalog/collection_cards.html', ctx)


def collection_detail(request, pk):
    collection = get_object_or_404(Collection, pk=pk)
    carpets = collection.carpets.all()
    return render(request, 'catalog/catalog_list.html', {
        'collection': collection,
        'carpets': carpets
    })