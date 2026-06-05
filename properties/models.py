from django.db import models
from django.contrib.auth.models import User


class Property(models.Model):
    TYPE_CHOICES = [
        ('apartment', 'شقة'),
        ('villa', 'فيلا'),
        ('office', 'مكتب'),
        ('land', 'أرض'),
        ('warehouse', 'مستودع'),
    ]
    STATUS_CHOICES = [
        ('sale', 'للبيع'),
        ('rent', 'للإيجار'),
    ]

    title = models.CharField(max_length=200, verbose_name='اسم العقار')
    description = models.TextField(verbose_name='وصف العقار', blank=True)
    price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='السعر')
    location = models.CharField(max_length=300, verbose_name='الموقع')
    area = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='المساحة (م²)')
    property_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='apartment', verbose_name='نوع العقار')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='sale', verbose_name='الحالة')
    bedrooms = models.PositiveIntegerField(default=0, verbose_name='غرف النوم')
    bathrooms = models.PositiveIntegerField(default=0, verbose_name='الحمامات')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='properties', verbose_name='المالك')
    created_at = models.DateTimeField(auto_now_add=True)
    is_available = models.BooleanField(default=True, verbose_name='متاح')

    # ── حقل الموافقة الجديد ──
    is_approved = models.BooleanField(default=False, verbose_name='معتمد من الإدارة')

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'عقار'
        verbose_name_plural = 'العقارات'

    def __str__(self):
        return self.title

    def get_primary_image(self):
        primary = self.images.filter(is_primary=True).first()
        if primary:
            return primary
        return self.images.first()

    @property
    def favorites_count(self):
        return self.favorites.count()


class PropertyImage(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='property_images/', verbose_name='الصورة')
    is_primary = models.BooleanField(default=False, verbose_name='الصورة الرئيسية')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'صورة العقار'
        verbose_name_plural = 'صور العقارات'

    def __str__(self):
        return f'صورة - {self.property.title}'


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='favorites')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'property')
        verbose_name = 'مفضلة'
        verbose_name_plural = 'المفضلات'

    def __str__(self):
        return f'{self.user.username} ← {self.property.title}'


class NegotiationRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'قيد الانتظار'),
        ('contacted', 'تم التواصل'),
        ('closed', 'مغلق'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='negotiations')
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='negotiations')
    message = models.TextField(verbose_name='رسالتك')
    phone = models.CharField(max_length=20, verbose_name='رقم الهاتف للتواصل')
    offered_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, verbose_name='السعر المقترح')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'طلب تفاوض'
        verbose_name_plural = 'طلبات التفاوض'

    def __str__(self):
        return f'{self.user.username} → {self.property.title}'
