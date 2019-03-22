"""
views for surveyadvance
"""
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
import json
from .forms import LoginForm, AdminForm, EventsForm
from .models import (Organization, org_Admin, Employee, Survey,
                    SurveyEmployee, SurveyQuestion, SurveyResponse)
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
import logging
import datetime

# Create your views here.
def index(request):
    return render(request, 'newsurvey/index.html')

@csrf_exempt
def login(request):
    form = LoginForm()
    context = {'form': form}

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

    try:
        usersdata = User.objects.filter(username=username, password=password)
        if(User.objects.filter(username=username).
                exists()):
            user = authenticate(username=username, password=password)
            return redirect('index')
        elif org_Admin.objects.get(admin_username=username, password=password):
            m = request.session['username'] = username
            return redirect('index')
        else:
            Employee.objects.filter(emp_username=username, emp_password=password)
            m = request.session['username'] = username
            return redirect('index')

    except Exception as e:
        print('Exception ', e)
        data = {'success': 'false', 'message': 'Invalid Username or Password'}
        return render(request, "newsurvey/login.html", context)

    return render(request, "newsurvey/login.html", context)


@csrf_exempt
def admin_register(request):
    """
    Admin register
    """
    form = AdminForm()
    context = {'form': form}
    if request.method == "POST":
        ad_username = request.POST.get("adminname")
        ad_password = request.POST.get("ad_password")
        m = request.POST.get('OrgnisationName')
        Org_names = Organization.objects.get(company_name=m)
        if request.POST.get('adminname') and request.POST.get('username')\
                and request.POST.get(
                'email') and request.POST.get('OrgnisationName') \
                and request.POST.get('password'):
            registerObject = org_Admin()
            registerObject.admin_name = request.POST.get('adminname')
            registerObject.admin_username = request.POST.get('username')
            registerObject.admin_email = request.POST.get('email')
            registerObject.company = Org_names
            registerObject.password = request.POST.get('password')
            registerObject.save()

        else:
            return redirect('admin_register')

    return render(request, "newsurvey/Org_adminlogin.html")


def logout(request):
    """
    Session logout
    """
    try:
        del request.session['username']
    except KeyError:
        pass
    return redirect('login')


def add_org(request):
    """
    add organization admin
    """
    if request.method == "POST":

        if request.POST.get('org_name') and request.POST.get('org_loc') \
                and request.POST.get('org_desc'):
            organization_object = Organization()
            organization_object.company_name = request.POST.get('org_name')
            organization_object.location = request.POST.get('org_loc')
            organization_object.description = request.POST.get('org_desc')

            organization_object.save()
            return redirect("add_org")
        else:
            return redirect('index')

    return render(request, "newsurvey/org.html")


def getorgdata(request):
    """
    get organisation list
    """
    org = list()
    org_details1 = Organization.objects.all()
    org.append(org_details1)
    i = 0
    temp_list = dict()
    data = {}
    for org1 in org_details1:
        i = i + 1
        temp_list[i] = [i, str(org1.company_name), str(org1.location), str(org1.description)]
    print("temp_list", temp_list)
    data = temp_list

    return HttpResponse(json.dumps(data), content_type="application/json")


def delete_org(request):
    """
    Delete particular org with org name.
    :param request:
    :return:
    """
    org_name = request.GET.get('company_name')
    org_record = Organization.objects.get(company_name=org_name)
    org_record.delete()
    return HttpResponse({'result': 'success'})


def upload_csv(request):
    """
    csv extract
    """
    data = {}
    if "GET" == request.method:
        return render(request, "newsurvey/emplist.html", data)
    # if not GET, then proceed
    try:
        csv_file = request.FILES["csv_file"]
        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'File is not CSV type')
            return HttpResponseRedirect(reverse("upload_csv"))
        # if file is too large, return
        if csv_file.multiple_chunks():
            messages.error(request, "Uploaded file is too big (%.2f MB)." % (csv_file.size / (1000 * 1000),))
            return HttpResponseRedirect(reverse("upload_csv"))

        file_data = csv_file.read().decode("utf-8")

        lines = file_data.split("\n")

        # loop over the lines and save them in db. If error , store as string and then display
        for line in lines:
            if line != "":
                fields = line.split(",")
                data_dict = {}
                data_dict["emp_name"] = fields[0]
                data_dict["emp_username"] = fields[1]
                data_dict["emp_password"] = fields[2]
                data_dict["emp_designation"] = fields[3]
                data_dict["emp_address"] = fields[4]
                data_dict["company"] = fields[5]
                m = (data_dict["company"]).strip()
                Org_names = Organization.objects.get(company_name=m)

                try:
                    form = EventsForm(data_dict)
                    org_employee_obj = Employee()
                    org_employee_obj.emp_name = data_dict["emp_name"]
                    org_employee_obj.emp_username = data_dict["emp_username"]
                    org_employee_obj.emp_password = data_dict["emp_password"]
                    org_employee_obj.emp_designation = data_dict["emp_designation"]
                    org_employee_obj.emp_address = data_dict["emp_address"]
                    org_employee_obj.company = Org_names

                    org_employee_obj.save()
                except Exception as e:
                    logging.getLogger("error_logger").error(repr(e))
                    pass

    except Exception as e:
        logging.getLogger("error_logger").error("Unable to upload file. " + repr(e))
        messages.error(request, "Unable to upload file. " + repr(e))

    return HttpResponseRedirect(reverse("upload_csv"))


def Add_Survey(request):
    """
    adding multiple surveys
    """
    if request.method == "POST":
        if request.POST.get('sur_name') \
                and request.POST.get('sur_desc'):

            survey_obj1 = Survey()
            survey_obj1.survey_name = request.POST.get('sur_name')
            survey_obj1.description = request.POST.get('sur_desc')
            survey_obj1.date = datetime.datetime.now()
            survey_obj1.save()
            return redirect("Add_Survey")
        else:
            return redirect('index')
    return render(request, 'newsurvey/addsurveypage.html')


def getSuvey_list(request):
    """
    getting survey list
    """
    total_survey = Survey.objects.all()
    context = {'total_survey': total_survey}
    return HttpResponse(json.dumps(list(context)), content_type="application/json")


def Assign_Survey(request):
    """
    assigning_survey
    :param request:
    :return:
    """
    survey_count = list()
    total_emplist = list()
    total_survey = Survey.objects.all()
    survey_count.append(total_survey)
    emp_list = Employee.objects.all()

    # for emp in emp_list:
    #     total_emplist.append(emp.emp_username)


    print("-------------register-submit----",emp_list.values_list()[0])
    # import pdb;pdb.set_trace()
    return render(request, 'newsurvey/assign_survey.html',
                  {'total_surveylist': total_survey,
                  'emplist': emp_list})

def store_assigned_surveys(request):
    """
    Store the multiple surveys assigned to employees in database.
    """
    surveys_list = list()
    emp_list = list()
    if request.method == 'POST':
        surveys_list = request.POST.getlist('surveys')
        emp_list = request.POST.getlist('employees')

        emp_objs = list()
        for emp in emp_list:
            emp_objs.append(Employee.objects.get(emp_username=emp))

        survey_objs = list()
        for survey in surveys_list:
            survey_objs.append(Survey.objects.get(survey_name=survey))

        print("suvryes",surveys_list)
        print("emp",emp_list)


        for survey in survey_objs:
            for emp in emp_objs:
                survey_emp_map = SurveyEmployee(survey=survey, employee=emp)
                survey_emp_map.save()

    elif request.method == 'GET':
        print(request.POST.getlist('surveys'))
        print(request.POST.getlist('employees'))
    return redirect('index')
