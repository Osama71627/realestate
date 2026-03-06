from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import Property, Favorite, NegotiationRequest
from .forms import NegotiationForm


def listing_view(request):
    properties = Property.objects.filter(is_available=True).prefetch_related('images')

    # Filters
    prop_type = request.GET.get('type', '')
    status = request.GET.get('status', '')
    search = request.GET.get('search', '')
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')

    if prop_type:
        properties = properties.filter(property_type=prop_type)
    if status:
        properties = properties.filter(status=status)
    if search:
        properties = properties.filter(title__icontains=search) | properties.filter(location__icontains=search)
    if min_price:
        properties = properties.filter(price__gte=min_price)
    if max_price:
        properties = properties.filter(price__lte=max_price)

    # Get user favorites ids
    favorite_ids = []
    if request.user.is_authenticated:
        favorite_ids = list(
            Favorite.objects.filter(user=request.user).values_list('property_id', flat=True)
        )

    context = {
        'properties': properties,
        'favorite_ids': favorite_ids,
        'total_count': properties.count(),
        'filters': {
            'type': prop_type,
            'status': status,
            'search': search,
            'min_price': min_price,
            'max_price': max_price,
        }
    }
    return render(request, 'properties/listing.html', context)


def detail_view(request, pk):
    property = get_object_or_404(Property, pk=pk)
    is_favorite = False
    if request.user.is_authenticated:
        is_favorite = Favorite.objects.filter(user=request.user, property=property).exists()

    context = {
        'property': property,
        'is_favorite': is_favorite,
        'images': property.images.all(),
    }
    return render(request, 'properties/detail.html', context)


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
    favorites = Favorite.objects.filter(user=request.user).select_related('property').prefetch_related('property__images')
    return render(request, 'properties/favorites.html', {'favorites': favorites})


@login_required
def negotiate_view(request, pk):
    property = get_object_or_404(Property, pk=pk)

    # Check if already sent
    existing = NegotiationRequest.objects.filter(user=request.user, property=property).first()

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
