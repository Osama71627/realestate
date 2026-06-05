from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .forms import RegisterForm, LoginForm


def register_view(request):
    # إذا كان الأدمن مسجّلاً، لا نسمح بتسجيل حساب جديد يطغى على جلسته
    if request.user.is_authenticated:
        if request.user.is_staff:
            messages.error(request, '⚠️ أنت مسجّل دخولك كمدير. افتح نافذة خاصة (Incognito) لاختبار حسابات أخرى.')
            return redirect('listing')
        return redirect('listing')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.first_name = form.cleaned_data['first_name']
            user.last_name  = form.cleaned_data['last_name']
            user.email      = form.cleaned_data['email']
            user.save()
            login(request, user)
            messages.success(request, f'مرحباً {user.first_name}! تم إنشاء حسابك بنجاح 🎉')
            return redirect('listing')
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    # ── حماية جلسة الأدمن ──────────────────────────────────────────────
    # إذا كان المستخدم الحالي أدمن، أوقف العملية فوراً
    if request.user.is_authenticated:
        if request.user.is_staff:#شرط هل هو ادمن 
            messages.error(
                request,
                '🛡️ أنت مسجّل دخولك كمدير. '
                'لاختبار حساب آخر استخدم نافذة خاصة (Incognito / Private).'
            )
            return redirect('listing')#اوقف العملية فورا 
        # مستخدم عادي مسجّل بالفعل
        return redirect('listing')
    # ────────────────────────────────────────────────────────────────────

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()

            # حماية إضافية: إذا كان المستخدم الحالي أدمن لا تسمح بالمتابعة
            # (حالة نادرة لكن نؤمّنها)
            if request.user.is_authenticated and request.user.is_staff:
                messages.error(request, '🛡️ لا يمكن تسجيل دخول مستخدم آخر أثناء جلسة المدير.')
                return redirect('listing')

            login(request, user)
            messages.success(request, f'أهلاً بعودتك، {user.first_name or user.username}!')
            return redirect(request.GET.get('next', 'listing'))
        else:
            messages.error(request, 'اسم المستخدم أو كلمة المرور غير صحيحة')
    else:
        form = LoginForm()

    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')
