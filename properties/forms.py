from django import forms
from .models import NegotiationRequest, Property


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


class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = [
            'title', 'property_type', 'status', 'price',
            'location', 'area', 'bedrooms', 'bathrooms', 'description'
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'مثال: شقة فاخرة في حي النخيل',
                'class': 'form-input'
            }),
            'property_type': forms.Select(attrs={'class': 'form-input'}),
            'status': forms.Select(attrs={'class': 'form-input'}),
            'price': forms.NumberInput(attrs={
                'placeholder': 'السعر بالريال السعودي',
                'class': 'form-input'
            }),
            'location': forms.TextInput(attrs={
                'placeholder': 'مثال: الرياض، حي النخيل، شارع الملك فهد',
                'class': 'form-input'
            }),
            'area': forms.NumberInput(attrs={
                'placeholder': 'المساحة بالمتر المربع',
                'class': 'form-input'
            }),
            'bedrooms': forms.NumberInput(attrs={
                'placeholder': '0',
                'class': 'form-input',
                'min': 0
            }),
            'bathrooms': forms.NumberInput(attrs={
                'placeholder': '0',
                'class': 'form-input',
                'min': 0
            }),
            'description': forms.Textarea(attrs={
                'placeholder': 'اكتب وصفاً تفصيلياً للعقار...',
                'class': 'form-input',
                'rows': 5
            }),
        }
        labels = {
            'title': 'اسم العقار',
            'property_type': 'نوع العقار',
            'status': 'حالة العقار',
            'price': 'السعر (ريال)',
            'location': 'الموقع',
            'area': 'المساحة (م²)',
            'bedrooms': 'عدد غرف النوم',
            'bathrooms': 'عدد الحمامات',
            'description': 'وصف العقار',
        }
