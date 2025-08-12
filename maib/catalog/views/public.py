from django.shortcuts import render, get_object_or_404
from django.db.models import Q, Case, When, Value, CharField, Count
from maib.catalog.models import Carpet, Collection
from django.core.paginator import Paginator
from django.db.models import Count, Min, Max

COLOR_FAMILIES = [
    {"key": "beige","label":"Бежевый / крем","hex":"#D8C9B2",
     "q": Q(color__icontains="BEIGE")|Q(color__icontains="BEJ")|Q(color__icontains="CREAM")|Q(color__icontains="IVORY")},
    {"key": "taupe","label":"Визон / тауп","hex":"#B7A9A1",
     "q": Q(color__icontains="VIZON")|Q(color__icontains="VİZON")|Q(color__icontains="TAUPE")|Q(color__icontains="GREIGE")},
    {"key": "grey","label":"Серый","hex":"#9AA0A6",
     "q": Q(color__icontains="GRAY")|Q(color__icontains="GREY")|Q(color__icontains="LGRAY")|Q(color__icontains="DGRAY")|Q(color__icontains="SMOKE")|Q(color__icontains="ASH")},
    {"key": "blue","label":"Синий / голубой","hex":"#3C79B5",
     "q": Q(color__icontains="BLUE")|Q(color__icontains="NAVY")|Q(color__icontains="SAXON")|Q(color__icontains="TURKUAZ")|Q(color__icontains="AQUA")|Q(color__icontains="MAVI")},
    {"key": "green","label":"Зелёный","hex":"#3F8F4E", "q": Q(color__icontains="GREEN")|Q(color__icontains="MINT")},
    {"key": "red","label":"Красный / бордо","hex":"#B23A48", "q": Q(color__icontains="RED")|Q(color__icontains="BORDO")|Q(color__icontains="MAROON")},
    {"key": "brown","label":"Коричневый","hex":"#8B5E3C", "q": Q(color__icontains="BROWN")|Q(color__icontains="COFFEE")|Q(color__icontains="CHOC")},
    {"key": "yellow","label":"Жёлтый / золото","hex":"#D6A20A", "q": Q(color__icontains="YELLOW")|Q(color__icontains="GOLD")},
    {"key": "orange","label":"Оранжевый / лосось","hex":"#F29B64", "q": Q(color__icontains="ORANGE")|Q(color__icontains="SOMON")},
    {"key": "purple","label":"Фиолетовый","hex":"#7D5BA6", "q": Q(color__icontains="PURPLE")|Q(color__icontains="VIOLET")},
    {"key": "pink","label":"Розовый","hex":"#E08EB4", "q": Q(color__icontains="PINK")},
    {"key": "bw","label":"Чёрный / белый","hex":"#333333", "q": Q(color__icontains="BLACK")|Q(color__icontains="WHITE")},
]

def carpet_list(request, pk=None):
    # базовая выборка
    qs_base = Carpet.objects.select_related('collection').all()

    # параметры
    q      = (request.GET.get('q') or '').strip()       # код
    color  = (request.GET.get('color') or '').strip()   # ключ семьи
    style  = (request.GET.get('style') or '').strip()

    # фильтр коллекции из URL
    if pk:
        qs_base = qs_base.filter(collection_id=pk)

    # поиск только по коду
    if q:
        qs_base = qs_base.filter(code__iexact=q)

    # аннотация цветовой семьи
    whens = [When(f["q"], then=Value(f["key"])) for f in COLOR_FAMILIES]
    qs_base = qs_base.annotate(
        color_family=Case(*whens, default=Value("other"), output_field=CharField())
    )

    # итоговая выборка с учётом выбранных фильтров
    qs = qs_base
    if style:
        qs = qs.filter(style__iexact=style)
    if color:
        qs = qs.filter(color_family=color)

    # стили — считаем БЕЗ учёта выбранного стиля (чтобы можно было переключиться)
    all_styles = list(
        qs_base.order_by('style').values_list('style', flat=True).distinct()
    )

    # цвета — можно учитывать выбранный стиль, чтобы список был релевантным
    fam_source = qs_base.filter(style__iexact=style) if style else qs_base
    fam_counts = dict(
        fam_source.values('color_family').annotate(cnt=Count('id')).values_list('color_family','cnt')
    )
    all_colors = [{**f, "count": fam_counts.get(f["key"], 0)}
                  for f in COLOR_FAMILIES if fam_counts.get(f["key"], 0)]

    # сортировка: новые сверху (created_at/id)
    fields = {f.name for f in Carpet._meta.get_fields()}
    age_field = 'created_at' if 'created_at' in fields else 'id'
    qs = qs.order_by(f'-{age_field}', 'id')

    # пагинация
    paginator = Paginator(qs, 12)
    page_obj = paginator.get_page(request.GET.get('page'))

    return render(request, 'catalog/catalog_list.html', {
        'page_obj': page_obj,
        'query': q,
        'color': color,
        'style': style,
        'all_colors': all_colors,   # [{key,label,hex,count}, …]
        'all_styles': all_styles,
    })

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