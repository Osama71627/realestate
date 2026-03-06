# 🏡 موقع العقارات - Django

## هيكل المشروع
```
realestate/
├── manage.py
├── requirements.txt
├── mysite/              ← إعدادات المشروع
├── accounts/            ← تسجيل الدخول وإنشاء الحساب
└── properties/          ← نظام العقارات
    ├── models.py        ← Property, PropertyImage, Favorite, NegotiationRequest
    ├── views.py         ← listing, detail, toggle_favorite, negotiate, my_favorites
    └── templates/
        ├── listing.html   ← الصفحة الرئيسية
        ├── detail.html    ← تفاصيل العقار
        ├── negotiate.html ← طلب التفاوض
        └── favorites.html ← المفضلة
```

## خطوات التشغيل

```bash
# 1. تثبيت المتطلبات
pip install -r requirements.txt

# 2. إنشاء الجداول
python manage.py makemigrations
python manage.py migrate

# 3. إنشاء Admin
python manage.py createsuperuser

# 4. تشغيل السيرفر
python manage.py runserver
```

## الصفحات
| الرابط | الوصف |
|--------|-------|
| `/login/` | تسجيل الدخول |
| `/register/` | إنشاء حساب |
| `/properties/` | الصفحة الرئيسية - كل العقارات |
| `/properties/<id>/` | تفاصيل عقار |
| `/properties/<id>/negotiate/` | طلب تفاوض |
| `/favorites/` | عقاراتي المفضلة |
| `/admin/` | لوحة إدارة العقارات |

## كيف تضيف عقاراً؟
1. افتح `/admin/`
2. اذهب لـ **Properties** → Add
3. أضف الصور من **Property Images** (Inline في نفس الصفحة)
4. احفظ ← يظهر العقار فوراً في الموقع ✅

## الميزات
- ✅ تسجيل دخول وإنشاء حساب مع ملف شخصي تلقائي
- ✅ عرض العقارات مع فلترة (نوع، حالة، سعر، بحث)
- ✅ صور متعددة لكل عقار مع معرض صور
- ✅ إضافة/حذف المفضلة
- ✅ طلب التفاوض مع المالك
- ✅ لوحة إدارة كاملة
