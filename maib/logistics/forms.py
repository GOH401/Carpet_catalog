from django import forms
from django.forms import inlineformset_factory
from .models import Batch, BatchItem

class BatchForm(forms.ModelForm):
    class Meta:
        model = Batch
        fields = [
            'arrival_date',
            'status',
            'storage_location',
            'destination',
        ]
        widgets = {
            'arrival_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'batch-form-input'
            }),
            'status': forms.Select(attrs={
                'class': 'batch-form-select'
            }),
            'storage_location': forms.TextInput(attrs={
                'class': 'batch-form-input',
                'placeholder': 'Например, Склад №3'
            }),
            'destination': forms.TextInput(attrs={
                'class': 'batch-form-input',
                'placeholder': 'Город, клиент или адрес'
            }),
        }

class BatchItemForm(forms.ModelForm):
    class Meta:
        model = BatchItem
        fields = ['carpet', 'quantity']
        widgets = {
            'carpet': forms.Select(attrs={'class': 'batch-form-select'}),
            'quantity': forms.NumberInput(attrs={'class': 'batch-form-input', 'min': '1'}),
        }

BatchItemFormSet = inlineformset_factory(
    Batch, BatchItem, form=BatchItemForm,
    extra=1, can_delete=True, min_num=1, validate_min=True
)
