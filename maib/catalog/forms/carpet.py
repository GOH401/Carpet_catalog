from django import forms
from maib.catalog.models import Carpet

PILE_HEIGHT_CHOICES = [('', '— Высота ворса —')] + [(f"{i} мм", f"{i} мм") for i in [4,6,8,10,12,15,20]]
DENSITY_CHOICES = [('', '— Плотность —')] + [(d, d) for d in [
    '180 000 точек/м²', '200 000 точек/м²', '224 000 точек/м²',
    '300 000 точек/м²', '400 000 точек/м²', '500 000 точек/м²'
]]
LOOM_WIDTH_CHOICES = [('', '— Ширина станка —'), ('4 м', '4 м'), ('5 м', '5 м')]

THREAD_MATERIAL_CHOICES = [
    ('', '— Выбрать —'),
    ('POLYESTER', 'POLYESTER'),
    ('PP', 'PP'),
    ('AKRIL', 'AKRIL'),
    ('ШЕРСТЬ', 'ШЕРСТЬ'),
    # добавь свои варианты
]

class CarpetForm(forms.ModelForm):
    pile_height = forms.ChoiceField(choices=PILE_HEIGHT_CHOICES, required=False, label="Высота ворса", widget=forms.Select(attrs={'class': 'carpet-form-select'}))
    density = forms.ChoiceField(choices=DENSITY_CHOICES, required=False, label="Плотность", widget=forms.Select(attrs={'class': 'carpet-form-select'}))
    loom_width = forms.ChoiceField(choices=LOOM_WIDTH_CHOICES, required=False, label="Ширина станка", widget=forms.Select(attrs={'class': 'carpet-form-select'}))
    yarn = forms.CharField(required=False, label="Пряжа", widget=forms.TextInput(attrs={'class': 'carpet-form-input'}))
    quality = forms.CharField(required=False, label="Качество", widget=forms.TextInput(attrs={'class': 'carpet-form-input'}))
    weight = forms.CharField(required=False, label="Вес (кг/м²)", widget=forms.TextInput(attrs={'class': 'carpet-form-input'}))

    # Заменяем thread_type на 4 отдельных поля
    thread_percent_left = forms.CharField(required=False, label="% 1", widget=forms.TextInput(attrs={'class': 'form-control'}))
    thread_material_left = forms.ChoiceField(required=False, label="Нить 1", choices=THREAD_MATERIAL_CHOICES, widget=forms.Select(attrs={'class': 'form-select'}))
    thread_percent_right = forms.CharField(required=False, label="% 2", widget=forms.TextInput(attrs={'class': 'form-control'}))
    thread_note = forms.CharField(required=False, label="Примечание", widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Carpet
        fields = [
            'collection', 'name', 'code', 'color', 'image', 'style',
            'loom_width', 'yarn', 'quality', 'pile_height', 'density',
            'weight', 'thread_percent_left', 'thread_material_left',
            'thread_percent_right', 'thread_note'
        ]
        widgets = {
            'collection': forms.Select(attrs={'class': 'carpet-form-select'}),
            'name': forms.TextInput(attrs={'class': 'carpet-form-input'}),
            'code': forms.TextInput(attrs={'class': 'carpet-form-input'}),
            'color': forms.TextInput(attrs={'class': 'carpet-form-input'}),
            'image': forms.ClearableFileInput(attrs={'class': 'carpet-form-input'}),
            'style': forms.Select(attrs={'class': 'carpet-form-select'}),
        }
