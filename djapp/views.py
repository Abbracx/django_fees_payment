from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.views.decorators.csrf import csrf_exempt

from djproj.logger import log
from djapp.forms import UserForm, DocumentForm
from djapp.models import Branch, UserProfileInfo, Fee, FeePaid, Orders, Document

from datetime import datetime

import razorpay
import json
import csv


@login_required
def index(request):
    """ Loads index page with user details and fee details """

    if request.method == 'POST':
        data = request.POST.getlist('fees')

        already_paid_ids = []
        fees = 0
        fee_name = ""
        for fee_id in data:
            fee_paid_obj = FeePaid.objects.filter(
                user_id=request.user.id, paid_fee_id=int(fee_id.split('_')[0]))
            if fee_paid_obj:
                already_paid_ids.append(fee_paid_obj[0].paid_fee.name)
            else:
                fee_obj = Fee.objects.filter(id=int(fee_id.split('_')[0]))[0]
                fees = fees + fee_obj.price
                if fee_name == "":
                    fee_name = fee_name + fee_obj.name
                else:
                    fee_name = fee_name + ", " + fee_obj.name

        if fees > 0:
            order = Orders.objects.create(user_id=request.user.id, name=order_name_by_index_val(
            ), amount=fees, fees_charged=fee_name)
            return HttpResponseRedirect(reverse('pay_fees', args=(order.name,)))
        else:
            try:
                portal_user = User.objects.get(username=request.user.username)
                fees = Fee.objects.all()
                return render(request, 'index.html', {
                    'fees_paid': 'There is nothing to Pay',
                    'portal_user': portal_user,
                    'user_form': UserForm(), 'fees': fees})
            except:
                return HttpResponseRedirect(reverse('payment_fail'))

    if request.method == 'GET':
        fee_paid_ids = FeePaid.objects.filter(
            user_id=request.user.id).values_list('paid_fee', flat=True)
        try:
            portal_user = User.objects.get(username=request.user.username)
            fees = Fee.objects.all()
            return render(request, 'index.html', {
                'portal_user': portal_user,
                'user_form': UserForm(),
                'fees': fees, 'fee_paid_ids': fee_paid_ids})
        except:
            return HttpResponseRedirect(reverse('payment_fail'))


@login_required
def user_logout(request):
    """ Logs out user """
    logout(request)
    return HttpResponseRedirect(reverse('index'))


def register(request):
    """ Handle registration of user """
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        if user_form.is_valid():
            firstname = user_form.cleaned_data.get('firstname')
            username = user_form.cleaned_data.get('username')
            lastname = user_form.cleaned_data.get('lastname')
            email = user_form.cleaned_data.get('email')
            password = user_form.cleaned_data.get('password')
            mobile = user_form.cleaned_data.get('mobile')
            enrollment = user_form.cleaned_data.get('enrollment')
            birth_date = user_form.cleaned_data.get('birth_date')
            branch = user_form.cleaned_data.get('branch')
            course = user_form.cleaned_data.get('course')
            gender = user_form.cleaned_data.get('gender')

            if not User.objects.filter(username=username):
                user = User.objects.create(
                    first_name=firstname, last_name=lastname,
                    username=username, email=email)
                user.set_password(password)
                user.save()
                if user:
                    if not UserProfileInfo.objects.filter(enrollment=enrollment):
                        UserProfileInfo.objects.create(
                            user=user, mobile=mobile, enrollment=enrollment,
                            birth_date=birth_date, course=course, gender=gender,
                            branch_id=branch.id)
                        login(request, user)
                        return redirect('index')
                    else:
                        return render(request, 'registration.html', {
                            'user_form': user_form,
                            'enroll_avl_err': 'User with this enrollment number already exists'
                        })
            else:
                return render(request, 'registration.html', {
                    'user_form': user_form,
                    'user_avl_err': 'User with this username already exists'
                })
        else:
            return render(request, 'registration.html', {
                'user_form': user_form,
                'errors': user_form.errors
            })
    else:
        user_form = UserForm()
    return render(request, 'registration.html', {'user_form': user_form})


def user_login(request):
    """ Handle Login """
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(request, 'login.html', {'error': 'Invalid login details given'})
    else:
        return render(request, 'login.html', {})


@csrf_exempt
def branch_list(request):
    """ Returns list of branches on AJAX call """
    branch_obj = Branch.objects.all().filter(
        institute_name_id=request.POST.get('branch_id'))
    branch_dict = dict()
    for branch in branch_obj.values('id', 'name'):
        branch_dict.update({str(branch.get('id')): str(branch.get('name'))})
    return JsonResponse(branch_dict)


@login_required
def pay_fees(request, order_name):
    """ Diaplays order name and total amount to be paid """
    order = Orders.objects.get(name=order_name)
    return render(request, 'payment.html', {'order': order, 'total_amount': int(order.amount) * 100})


def order_name_by_index_val():
    """ Generates unique order id to send in payment gateway """
    try:
        index_val = Orders.objects.latest('id').id
        index_val = index_val + 1
    except:
        index_val = 1
    return "Order_" + str(index_val)


@login_required
def payment_success(request):
    """ Redirects to payment success page """
    return render(request, 'success.html')


@login_required
def payment_fail(request):
    """ Redirects to payment error page """
    return render(request, 'error.html')


def create_fee_paid(order):
    """ Marks fee as paid after successfull payment """
    try:
        fees = order.fees_charged.split(',')
        for i in range(0, len(fees)):
            fee_id = Fee.objects.filter(name=fees[i].lstrip())[0].id
            FeePaid.objects.create(
                user_id=order.user.id, paid_fee_id=fee_id)
        return True
    except:
        return HttpResponseRedirect(reverse('payment_fail'))


@csrf_exempt
def charge(request):
    """ After payment this method confirms if payment made is valid or not
        Also saves json dump of response into a field
    """
    razorpay_client = razorpay.Client(
        auth=("rzp_test_pMQIIt4C03HoRt", "OEabePWspOIHgWl0KXReutrH"))
    payment_id = request.POST.get('razorpay_payment_id')
    order = Orders.objects.get(name=request.POST.get('shopping_order_id'))
    order.razorpay_id = payment_id
    order.save()
    try:
        order.razorpay_dump = json.dumps(
            razorpay_client.payment.fetch(payment_id))
        razorpay_client.payment.capture(payment_id, int(order.amount) * 100)
        order.save()
        create_fee_paid(order)
        return HttpResponseRedirect(reverse('payment_success'))
    except:
        order.razorpay_dump = json.dumps(
            razorpay_client.payment.fetch(payment_id))
        order.save()
        return HttpResponseRedirect(reverse('payment_fail'))


@login_required
def import_user(request):
    """
    Imports user from CSV file
    Fields: first_name, last_name, username, email, password, birthdate,
            mobile_no, enrollment, branch, course, gender
    """
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Document(docfile=request.FILES['docfile'])
            newdoc.save()
            file_path = newdoc.docfile.path
            if file_path.split('.')[-1] == "csv":
                file = open(file_path, "r")
                lines = csv.reader(file)
                import_error = list()
                for index, data in enumerate(lines):
                    if index:
                        user = User.objects.filter(username=str(data[2]))
                        user_profile = UserProfileInfo.objects.filter(
                            enrollment=str(data[7]))
                        if user or user_profile:
                            if user:
                                import_error.append(
                                    "Line " + str(index) + " :- User with username '" + str(data[2]) + "' already exists")
                            else:
                                import_error.append(
                                    "Line " + str(index) + " :- User profile with enrollment number '" + str(data[7]) + "' already exists")
                        else:
                            user = User.objects.create(first_name=str(data[0]), email=str(data[3]),
                                                       last_name=str(data[1]), username=str(data[2]))
                            user.set_password(str(data[4]))
                            user.save()
                            if user:
                                birthdate = datetime.strptime(
                                    str(data[5]), '%d-%m-%Y')
                                branch_id = Branch.objects.filter(
                                    slug=str(data[8]))
                                user_profile = UserProfileInfo.objects.create(
                                    user=user, birth_date=birthdate, mobile=str(data[
                                                                                6]),
                                    enrollment=str(data[7]), branch=branch_id[0],
                                    course=str(data[9]), gender=str(data[10]))

                if import_error:
                    error_list = '<br/>'.join(import_error)
                    error_list = mark_safe(error_list)
                    return render(request, 'import.html', {'import_error': error_list})
                else:
                    return render(request, 'import.html', {'success': "Data imported successfully"})
            return render(request, 'import.html', {'file_error': "Only CSV file is allowed."})
    else:
        form = DocumentForm()
    return render(request, 'import.html', {'form': form})
