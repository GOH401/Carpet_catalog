# maib/catalog/forms/collection_form.py
from django import forms
from maib.catalog.models.collection import Collection

class CollectionForm(forms.ModelForm):
    class Meta:
        model = Collection
        fields = ['name', 'image_url', 'main_colors']  # убедись, что image_url есть в модели
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control form-control-lg'}),
            'image_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://.../collections/cover.jpg'}),
            'main_colors': forms.HiddenInput(),  # будем управлять этим полем через JS
        }
        labels = {
            'image_url': 'Изображение превью (URL)',
        }

    def clean_main_colors(self):
        raw = self.cleaned_data.get('main_colors', '')
        colors = [c.strip() for c in raw.split(',') if c.strip()]
        if len(colors) > 8:
            raise forms.ValidationError("Максимум 8 цветов.")
        for color in colors:
            if not color.startswith('#') or len(color) not in (4, 7):
                raise forms.ValidationError(f"Неверный формат цвета: {color}")
        return ', '.join(colors)
