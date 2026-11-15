from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q
from .models import Scheme, SchemeApplication
from .forms import SchemeForm, SchemeApplicationForm, SchemeSearchForm


EDUCATION_ORDER = ['below_10', '10th', '12th', 'graduate', 'postgraduate']


def home(request):
    schemes = Scheme.objects.filter(status='active')[:6]
    categories = dict(Scheme._meta.get_field('category').choices)
    return render(request, 'home.html', {'schemes': schemes, 'categories': categories})


def scheme_list(request):
    schemes = Scheme.objects.filter(status='active')
    form = SchemeSearchForm(request.GET)
    if form.is_valid():
        q = form.cleaned_data.get('q')
        category = form.cleaned_data.get('category')
        if q:
            schemes = schemes.filter(Q(name__icontains=q) | Q(description__icontains=q))
        if category:
            schemes = schemes.filter(category=category)
    return render(request, 'schemes/scheme_list.html', {'schemes': schemes, 'form': form})


def scheme_detail(request, pk):
    scheme = get_object_or_404(Scheme, pk=pk, status='active')
    already_applied = False
    if request.user.is_authenticated:
        already_applied = SchemeApplication.objects.filter(user=request.user, scheme=scheme).exists()
    return render(request, 'schemes/scheme_detail.html', {
        'scheme': scheme,
        'already_applied': already_applied,
    })


def scheme_detail_slug(request, slug):
    scheme = get_object_or_404(Scheme, slug=slug, status='active')
    already_applied = False
    if request.user.is_authenticated:
        already_applied = SchemeApplication.objects.filter(user=request.user, scheme=scheme).exists()
    return render(request, 'schemes/scheme_detail.html', {
        'scheme': scheme,
        'already_applied': already_applied,
    })


def scheme_by_category(request, category):
    schemes = Scheme.objects.filter(status='active', category=category)
    category_display = dict(Scheme._meta.get_field('category').choices).get(category, category)
    return render(request, 'schemes/scheme_list.html', {
        'schemes': schemes,
        'category_name': category_display,
        'form': SchemeSearchForm(),
    })


def schemes_by_year(request, year):
    schemes = Scheme.objects.filter(status='active', created_at__year=year)
    return render(request, 'schemes/scheme_list.html', {
        'schemes': schemes,
        'category_name': f'Schemes from {year}',
        'form': SchemeSearchForm(),
    })


def scheme_api_list(request):
    schemes = Scheme.objects.filter(status='active').values(
        'id', 'name', 'slug', 'category', 'organization', 'status', 'created_at'
    )
    return JsonResponse({'schemes': list(schemes)}, safe=False)


@login_required
def scheme_apply(request, pk):
    scheme = get_object_or_404(Scheme, pk=pk, status='active')
    if SchemeApplication.objects.filter(user=request.user, scheme=scheme).exists():
        messages.warning(request, 'You have already applied to this scheme.')
        return redirect('scheme_detail', pk=pk)
    if request.method == 'POST':
        form = SchemeApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.user = request.user
            application.scheme = scheme
            application.save()
            messages.success(request, 'Application submitted successfully!')
            return redirect('my_applications')
    else:
        form = SchemeApplicationForm()
    return render(request, 'schemes/scheme_apply.html', {'form': form, 'scheme': scheme})


@login_required
def my_applications(request):
    applications = SchemeApplication.objects.filter(user=request.user).select_related('scheme')
    return render(request, 'schemes/my_applications.html', {'applications': applications})


@login_required
def matched_schemes(request):
    profile = getattr(request.user, 'profile', None)
    if not profile or not profile.is_complete():
        messages.warning(request, 'Please complete your profile to see matched schemes.')
        return redirect('profile')

    schemes = Scheme.objects.filter(status='active')
    matched = []
    for scheme in schemes:
        score = 0
        total = 0

        if scheme.min_age or scheme.max_age:
            total += 1
            if profile.age:
                age_ok = True
                if scheme.min_age and profile.age < scheme.min_age:
                    age_ok = False
                if scheme.max_age and profile.age > scheme.max_age:
                    age_ok = False
                if age_ok:
                    score += 1

        if scheme.max_income:
            total += 1
            if profile.annual_income is not None and profile.annual_income <= scheme.max_income:
                score += 1

        if scheme.eligible_genders:
            total += 1
            genders = [g.strip() for g in scheme.eligible_genders.split(',')]
            if profile.gender in genders:
                score += 1

        if scheme.eligible_categories:
            total += 1
            categories = [c.strip() for c in scheme.eligible_categories.split(',')]
            if profile.category in categories:
                score += 1

        if scheme.min_education:
            total += 1
            if profile.education:
                user_idx = EDUCATION_ORDER.index(profile.education) if profile.education in EDUCATION_ORDER else -1
                req_idx = EDUCATION_ORDER.index(scheme.min_education) if scheme.min_education in EDUCATION_ORDER else -1
                if user_idx >= req_idx:
                    score += 1

        match_pct = int((score / total) * 100) if total > 0 else 100
        if match_pct >= 60:
            matched.append({'scheme': scheme, 'match_percentage': match_pct})

    matched.sort(key=lambda x: x['match_percentage'], reverse=True)
    return render(request, 'schemes/matched_schemes.html', {'matched': matched})


@login_required
def scheme_create(request):
    if not request.user.is_staff:
        messages.error(request, 'Only organizers can create schemes.')
        return redirect('home')
    if request.method == 'POST':
        form = SchemeForm(request.POST)
        if form.is_valid():
            scheme = form.save(commit=False)
            scheme.created_by = request.user
            scheme.save()
            messages.success(request, 'Scheme created successfully!')
            return redirect('scheme_detail', pk=scheme.pk)
    else:
        form = SchemeForm()
    return render(request, 'schemes/scheme_create.html', {'form': form})


@login_required
def scheme_edit(request, pk):
    scheme = get_object_or_404(Scheme, pk=pk)
    if not request.user.is_staff and scheme.created_by != request.user:
        messages.error(request, 'You do not have permission to edit this scheme.')
        return redirect('home')
    if request.method == 'POST':
        form = SchemeForm(request.POST, instance=scheme)
        if form.is_valid():
            form.save()
            messages.success(request, 'Scheme updated successfully!')
            return redirect('scheme_detail', pk=scheme.pk)
    else:
        form = SchemeForm(instance=scheme)
    return render(request, 'schemes/scheme_create.html', {'form': form, 'editing': True, 'scheme': scheme})


@login_required
def manage_applications(request):
    if not request.user.is_staff:
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('home')
    if request.user.is_superuser:
        applications = SchemeApplication.objects.all().select_related('user', 'scheme')
    else:
        applications = SchemeApplication.objects.filter(
            scheme__created_by=request.user
        ).select_related('user', 'scheme')

    status_filter = request.GET.get('status', '')
    if status_filter:
        applications = applications.filter(status=status_filter)

    return render(request, 'schemes/manage_applications.html', {
        'applications': applications,
        'status_filter': status_filter,
    })


@login_required
def approve_application(request, pk):
    if not request.user.is_staff:
        messages.error(request, 'You do not have permission.')
        return redirect('home')
    application = get_object_or_404(SchemeApplication, pk=pk)
    if request.method == 'POST':
        application.status = 'approved'
        application.admin_remarks = request.POST.get('remarks', '')
        application.save()
        messages.success(request, f'Application by {application.user.username} approved.')
    return redirect('manage_applications')


@login_required
def reject_application(request, pk):
    if not request.user.is_staff:
        messages.error(request, 'You do not have permission.')
        return redirect('home')
    application = get_object_or_404(SchemeApplication, pk=pk)
    if request.method == 'POST':
        application.status = 'rejected'
        application.admin_remarks = request.POST.get('remarks', '')
        application.save()
        messages.success(request, f'Application by {application.user.username} rejected.')
    return redirect('manage_applications')


def custom_404(request, exception):
    return render(request, '404.html', status=404)


def custom_500(request):
    return render(request, '500.html', status=500)
