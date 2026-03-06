from django import forms
from .models import NegotiationRequest


class NegotiationForm(forms.ModelForm):
    class Meta:
        model = NegotiationRequest
        fields = ['phone', 'offered_price', 'message']
        widgets = {
            'phone': forms.TextInput(attrs={
                'placeholder': 'مثال: 0512345678',
                'class': 'form-input'
            }),
            'offered_price': forms.NumberInput(attrs={
                'placeholder': 'السعر المقترح (اختياري)',
                'class': 'form-input'
            }),
            'message': forms.Textarea(attrs={
                'placeholder': 'اكتب رسالتك هنا...',
                'class': 'form-input',
                'rows': 4
            }),
        }
        labels = {
            'phone': 'رقم الهاتف',
            'offered_price': 'السعر المقترح (ريال)',
            'message': 'رسالتك للمالك',
        }
