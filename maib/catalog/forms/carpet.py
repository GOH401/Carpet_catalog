# maib/catalog/forms/carpet.py
from django import forms
from maib.catalog.models import Carpet

PILE_HEIGHT_CHOICES = [('', '— Высота ворса —')] + [(f"{i} мм", f"{i} мм") for i in [4, 6, 8, 10, 12, 15, 20]]
LOOM_WIDTH_CHOICES  = [('', '— Ширина станка —'), ('4 м', '4 м'), ('5 м', '5 м')]
THREAD_MATERIAL_CHOICES = [
    ('', '— Выбрать —'), ('POLYESTER', 'POLYESTER'), ('PP', 'PP'), ('AKRIL', 'AKRIL'), ('ШЕРСТЬ', 'ШЕРСТЬ'),
]

class CarpetForm(forms.ModelForm):
    # image — URL (альтернатива загрузке)
    image = forms.URLField(
        required=False, label="Изображение (URL)",
        widget=forms.URLInput(attrs={'placeholder': 'https://…/F053D_BLUE_BLUE.jpg'})
    )
    # upload — файл (уходит в Supabase; в вьюхе он имеет приоритет над URL)
    upload = forms.ImageField(required=False, label="Загрузить файл")

    pile_height = forms.ChoiceField(choices=PILE_HEIGHT_CHOICES, required=False, label="Высота ворса")
    loom_width  = forms.ChoiceField(choices=LOOM_WIDTH_CHOICES,  required=False, label="Ширина станка")

    # Состав (как в карточке)
    thread_percent_left  = forms.CharField(required=False, label="% 1")
    thread_material_left = forms.ChoiceField(required=False, label="Нить 1", choices=THREAD_MATERIAL_CHOICES)
    thread_percent_right = forms.CharField(required=False, label="% 2")
    thread_note          = forms.CharField(required=False, label="Примечание")

    class Meta:
        model = Carpet
        fields = [
            'collection', 'name', 'code', 'color',
            'image', 'upload', 'style',
            'loom_width', 'quality', 'pile_height', 'weight',
            'thread_percent_left', 'thread_material_left',
            'thread_percent_right', 'thread_note',
        ]
        widgets = {
            'collection': forms.Select(),
            'name':       forms.TextInput(),
            'code':       forms.TextInput(),
            'color':      forms.TextInput(),
            'style':      forms.Select(),
            'quality':    forms.TextInput(),
            'weight':     forms.TextInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # аккуратные bootstrap-классы
        for f in self.fields.values():
            if isinstance(f.widget, (forms.Select, forms.SelectMultiple)):
                f.widget.attrs.setdefault('class', 'form-select')
            else:
                f.widget.attrs.setdefault('class', 'form-control')
