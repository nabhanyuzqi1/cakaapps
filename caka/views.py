from django.shortcuts import redirect, render
from caka.models import Categories, Course, Level
from django.template.loader import render_to_string
from django.http import JsonResponse


def BASE(request):
    category = Categories.get_all_category(Categories)
    course = Course.objects.all()
    context = {
        'category': category,
        'course': course,
    }
    return render(request, 'base.html', context)


def HOME(request):
    category = Categories.objects.all().order_by('id')[0:5]
    course = Course.objects.filter(status='PUBLISH').order_by('-id')

    context = {
        'category': category,
        'course': course,
    }
    return render(request, 'Main/home.html', context)

def LIST_COURSE(request):
    category = Categories.get_all_category(Categories)
    level = Level.objects.all()
    course = Course.objects.all()
    freecourse_count = Course.objects.filter(price=0).count()
    paidcourse_count = Course.objects.filter(price__gte=1).count()
    membershipcourse_count = Course.objects.filter(price__gte=2).count()

    context = {
        'category': category,
        'level': level,
        'course': course,
        'freecourse_count': freecourse_count,
    }
    return render(request, 'Main/list_course.html', context)


def filter_data(request):
    categories = request.GET.getlist('category[]')
    level = request.GET.getlist('level[]')
    price = request.GET.getlist('price[]')


    if price == ['pricefree']:
        course = Course.objects.filter(price=0)
    elif price == ['pricepaid']:
        course = Course.objects.filter(price__gte=1)
    elif price == ['priceall']:
        course = Course.objects.all()
    elif price == ['pricemembership']:
        course = Course.objects.filter(price__gte=2)
    elif categories:
        course = Course.objects.filter(category__id__in=categories).order_by('-id')
    elif level:
        course = Course.objects.filter(level__id__in=level).order_by('-id')
    else:
        course = Course.objects.all().order_by('-id')

    t = render_to_string('ajax/course.html', {'course': course})

    return JsonResponse({'data': t})


def CONTACT_US(request):
    category = Categories.get_all_category(Categories)
    course = Course.objects.all()
    context = {
        'category': category,
        'course': course,
    }
    return render(request, 'Main/contact_us.html',context)


def ABOUT_US(request):
    category = Categories.get_all_category(Categories)
    course = Course.objects.all()
    context = {
        'category': category,
        'course': course,
    }
    return render(request, 'Main/about_us.html', context)


def CUSTOM_LOGIN(request):
    return render(request, 'registration/custom/login_custom.html')


def SEARCH_COURSE(request):
    category = Categories.get_all_category(Categories)
    query = request.GET['query']
    course = Course.objects.filter(title__icontains=query)


    context = {
        'category': category,
        'course': course,
        'query': query
    }
    return render(request, 'search/search.html',context)


def COURSE_DETAILS(request, slug):
    category = Categories.get_all_category(Categories)
    course = Course.objects.filter(slug = slug)
    if course.exists():
        course = course.first()
    else:
        return redirect('404')

    context = {
        'category': category,
        'course': course,
    }
    return render(request, 'course/course_details.html', context)


def PAGE_NOT_FOUND(request):
    category = Categories.get_all_category(Categories)
    course = Course.objects.all()
    context = {
        'category': category,
        'course': course,
    }
    return render(request, 'error/404.html', context)


def WEB_CHECK(request):
    return render(request, 'custom/release_checklist.html')