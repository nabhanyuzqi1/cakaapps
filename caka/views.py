import datetime

from django.shortcuts import redirect, render
from caka.models import Categories, Course, Level, Video, UserCourse, generate_random_string, Payment
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.db.models import Sum
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from time import time
from midtransclient import *

MERCHANT_ID = "G787824232"
CLIENT_KEY = "SB-Mid-client-DWewtoL9TgDMVTHn"
SERVER_KEY = "SB-Mid-server-YkLpYgXsx_JCscPIMq1MfrEU"

snap = Snap(
    is_production=False,
    server_key=SERVER_KEY,
    client_key=CLIENT_KEY
)

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
    time_duration = Video.objects.filter(course__slug=slug).aggregate(sum=Sum('time_duration'))

    course_id = Course.objects.get(slug=slug)
    try:
        check_enroll = UserCourse.objects.get(user = request.user, course = course_id)
    except UserCourse.DoesNotExist:
        check_enroll = None

    course = Course.objects.filter(slug=slug)
    if course.exists():
        course = course.first()
    else:
        return redirect('404')

    context = {
        'category': category,
        'course': course,
        'time_duration': time_duration,
        'check_enroll': check_enroll,
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


def CHECKOUT(request, slug):
    course = Course.objects.get(slug=slug)
    action = request.GET.get('action')
    order_id = generate_random_string(11)
    order = None

    if course.price == 0:
        course = UserCourse (
            user = request.user,
            course = course,
        )
        messages.success(request,'Course Are Successfully Enrolled !')
        course.save()
        return redirect('my_course')

    elif action == 'create_payment':
        if request.method == "POST":
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            country = request.POST.get('country')
            address_1 = request.POST.get('address_1')
            address_2 = request.POST.get('address_2')
            city = request.POST.get('city')
            postcode = request.POST.get('postcode')
            phone = request.POST.get('phone')
            email = request.POST.get('email')
            order_comments = request.POST.get('order_comments')
            amount = course.price
            currency = "IDR"
            receipt = f"Caka-{int(time())}"


            param = {
                "transaction_details": {
                    "order_id": order_id,
                    "gross_amount": amount
                }, "credit_card": {
                    "secure": True
                }
            }

            # create transaction
            order = snap.create_transaction(param)
            # transaction token
            SNAP_TOKEN = order['token']
            print('transaction_token:')
            print(SNAP_TOKEN)

            payment = Payment(
                course = course,
                user = request.user,
                order_id = order_id,
                payment_id = SNAP_TOKEN,
            )
            payment.save()
            get_token = Payment.objects.get(payment_id=SNAP_TOKEN)

    context = {
        'course': course,
        'order': order,
        'SNAP_TOKEN': SNAP_TOKEN
    }
    return render(request, 'checkout/checkout.html', context)


def MY_COURSE(request):
    category = Categories.get_all_category(Categories)
    course = UserCourse.objects.filter(user=request.user)
    context = {
        'category': category,
        'course': course,
    }
    return render(request, 'course/my-course.html', context)

@csrf_exempt
def VERIFY_PAYMENT(request):
    if request.method == "POST":
        data = request.POST
        print(data)
        client.transactions.status()
    return None