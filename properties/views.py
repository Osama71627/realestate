from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import JsonResponse
from .models import Property, PropertyImage, Favorite, NegotiationRequest
from .forms import NegotiationForm, PropertyForm


# ── مساعد: هل المستخدم أدمن؟ ──
def is_admin(user):
    return user.is_authenticated and user.is_staff


# ─────────────────────────────────────────
# صفحة قائمة العقارات
# ─────────────────────────────────────────
def listing_view(request):
    # يعرض فقط العقارات المعتمدة والمتاحة
    properties = Property.objects.filter(
        is_available=True, is_approved=True
    ).prefetch_related('images')

    prop_type  = request.GET.get('type', '')
    status     = request.GET.get('status', '')
    search     = request.GET.get('search', '')
    min_price  = request.GET.get('min_price', '')
    max_price  = request.GET.get('max_price', '')

    if prop_type:
        properties = properties.filter(property_type=prop_type)
    if status:
        properties = properties.filter(status=status)
    if search:
        properties = (
            properties.filter(title__icontains=search) |
            properties.filter(location__icontains=search)
        )
    if min_price:
        properties = properties.filter(price__gte=min_price)
    if max_price:
        properties = properties.filter(price__lte=max_price)

    favorite_ids = []
    if request.user.is_authenticated:
        favorite_ids = list(
            Favorite.objects.filter(user=request.user)
            .values_list('property_id', flat=True)
        )

    # عدد العقارات المعلقة للأدمن
    pending_count = 0
    if request.user.is_authenticated and request.user.is_staff:
        pending_count = Property.objects.filter(is_approved=False).count()

    context = {
        'properties': properties,
        'favorite_ids': favorite_ids,
        'total_count': properties.count(),
        'pending_count': pending_count,
        'filters': {
            'type': prop_type,
            'status': status,
            'search': search,
            'min_price': min_price,
            'max_price': max_price,
        }
    }
    return render(request, 'properties/listing.html', context)


# ─────────────────────────────────────────
# تفاصيل العقار
# ─────────────────────────────────────────
def detail_view(request, pk):
    property = get_object_or_404(Property, pk=pk)
    is_favorite = False
    if request.user.is_authenticated:
        is_favorite = Favorite.objects.filter(
            user=request.user, property=property
        ).exists()

    context = {
        'property': property,
        'is_favorite': is_favorite,
        'images': property.images.all(),
    }
    return render(request, 'properties/detail.html', context)


# ─────────────────────────────────────────
# نشر عقار جديد (مستخدم عادي)
# ─────────────────────────────────────────
@login_required
def create_property_view(request):
    if request.method == 'POST':
        form = PropertyForm(request.POST)
        images = request.FILES.getlist('images')

        if form.is_valid():
            prop = form.save(commit=False)
            prop.created_by = request.user
            prop.is_approved = False   # ينتظر موافقة الأدمن
            prop.is_available = True
            prop.save()

            # حفظ الصور إن وُجدت
            for i, img_file in enumerate(images):
                PropertyImage.objects.create(
                    property=prop,
                    image=img_file,
                    is_primary=(i == 0)
                )

            messages.success(
                request,
                '✅ تم إرسال العقار بنجاح! سيظهر في الموقع بعد مراجعة وموافقة الإدارة.'
            )
            return redirect('listing')
    else:
        form = PropertyForm()

    return render(request, 'properties/create.html', {'form': form})


# ─────────────────────────────────────────
# لوحة الأدمن — مراجعة العقارات المعلقة
# ─────────────────────────────────────────
@login_required
@user_passes_test(is_admin, login_url='listing')
def admin_dashboard_view(request):
    pending    = Property.objects.filter(is_approved=False).prefetch_related('images').select_related('created_by')
    approved   = Property.objects.filter(is_approved=True).prefetch_related('images').select_related('created_by')
    context = {
        'pending': pending,
        'approved': approved,
        'pending_count': pending.count(),
    }
    return render(request, 'properties/admin_dashboard.html', context)


# ─────────────────────────────────────────
# قبول عقار
# ─────────────────────────────────────────
@login_required
@user_passes_test(is_admin, login_url='listing')
def approve_property_view(request, pk):
    prop = get_object_or_404(Property, pk=pk)
    prop.is_approved = True
    prop.save()
    messages.success(request, f'✅ تم قبول ونشر العقار: {prop.title}')
    return redirect('admin_dashboard')


# ─────────────────────────────────────────
# رفض / حذف عقار
# ─────────────────────────────────────────
@login_required
@user_passes_test(is_admin, login_url='listing')
def reject_property_view(request, pk):
    prop = get_object_or_404(Property, pk=pk)
    title = prop.title
    prop.delete()
    messages.success(request, f'🗑️ تم رفض وحذف العقار: {title}')
    return redirect('admin_dashboard')


# ─────────────────────────────────────────
# المفضلة
# ─────────────────────────────────────────
@login_required
def toggle_favorite(request, pk):
    property = get_object_or_404(Property, pk=pk)
    fav, created = Favorite.objects.get_or_create(user=request.user, property=property)
    if not created:
        fav.delete()
        is_favorite = False
        msg = 'تم الحذف من المفضلة'
    else:
        is_favorite = True
        msg = 'تمت الإضافة إلى المفضلة ❤️'

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'is_favorite': is_favorite, 'message': msg})

    messages.success(request, msg)
    return redirect(request.META.get('HTTP_REFERER', 'listing'))


@login_required
def my_favorites(request):
    favorites = (
        Favorite.objects
        .filter(user=request.user)
        .select_related('property')
        .prefetch_related('property__images')
    )
    return render(request, 'properties/favorites.html', {'favorites': favorites})


# ─────────────────────────────────────────
# عقاراتي — كل العقارات التي نشرها المستخدم
# ─────────────────────────────────────────
@login_required
def my_properties(request):
    # نجلب كل عقارات هذا المستخدم سواء معتمدة أو معلقة
    props = (
        Property.objects
        .filter(created_by=request.user)   # فلتر بالمالك فقط
        .prefetch_related('images')        # جلب الصور بكفاءة
        .order_by('-created_at')           # الأحدث أولاً
    )
    context = {
        'my_props': props,
        'total': props.count(),
        'approved_count': props.filter(is_approved=True).count(),
        'pending_count': props.filter(is_approved=False).count(),
    }
    return render(request, 'properties/my_properties.html', context)


# ─────────────────────────────────────────
# طلب التفاوض
# ─────────────────────────────────────────
@login_required
def negotiate_view(request, pk):
    property = get_object_or_404(Property, pk=pk)
    existing = NegotiationRequest.objects.filter(
        user=request.user, property=property
    ).first()

    if request.method == 'POST':
        form = NegotiationForm(request.POST)
        if form.is_valid():
            neg = form.save(commit=False)
            neg.user = request.user
            neg.property = property
            neg.save()
            messages.success(request, 'تم إرسال طلب التفاوض بنجاح! سيتواصل معك المالك قريباً ✅')
            return redirect('detail', pk=pk)
    else:
        form = NegotiationForm()

    return render(request, 'properties/negotiate.html', {
        'form': form,
        'property': property,
        'existing': existing,
    })
