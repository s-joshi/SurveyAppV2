"""
views for surveyadvance
"""
import json
import logging
import datetime
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.core.paginator import (Paginator, EmptyPage, PageNotAnInteger)
from django.contrib import auth
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from .forms import (LoginForm, AdminForm, EventsForm)
from .models import (Organization, org_Admin, Employee, Survey,
                     SurveyEmployee, SurveyQuestion, SurveyResponse, Question)

surveys_completion_count = dict()

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
        if(User.objects.filter(username=username).
                exists()):
            user = auth.authenticate(username=username, password=password)
            auth.login(request, user)
            return redirect('index')
        try:
            org_admin_obj = org_Admin.objects.get(admin_username=username,
                                                  password=password)
            request.session['username'] = org_admin_obj.admin_username
            request.session['org_name'] = org_admin_obj.company.company_name
            return redirect('index')
        except Exception as e:
            print("Org admin with this username and password not available.")
            print(e)
            try:
                Employee.objects.get(emp_username=username,
                                     emp_password=password)
                request.session['username'] = username
                return redirect('emp_survey_assign')
            except Exception as e:
                print("No Emp available")

    except Exception as e:
        print('Exception ', e)
        data = {'success': 'false', 'message': 'Invalid Username or Password'}
        return render(request, "newsurvey/login.html", context)

    return render(request, "newsurvey/login.html", context)


def admin_register(request):
    """
    Admin register
    """
    form = AdminForm()
    context = {'form': form}
    org_list = Organization.objects.all()
    if request.method == "POST":
        # ad_username = request.POST.get("adminname")
        # ad_password = request.POST.get("ad_password")
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

    return render(request, "newsurvey/Org_adminlogin.html", {
        'org_total': org_list})


def logout(request):
    """
    Session logout
    """
    try:
        if request.user.is_superuser:
            auth.logout(request)
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
    # data = {}
    for org1 in org_details1:
        i = i + 1
        temp_list[i] = [i, str(org1.company_name), str(org1.location),
                        str(org1.description)]
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
    import pdb;pdb.set_trace()
    if request.method == 'GET':
        return render(request, "newsurvey/emp_csv.html", data)
    # if not GET, then proceed
    try:
        csv_file = request.FILES["csv_file"]
        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'File is not CSV type')
            return HttpResponseRedirect(reverse("emp_upload_csv"))

        # if file is too large, return
        if csv_file.multiple_chunks():
            messages.error(request, "Uploaded file is too big (%.2f MB)." % (
                csv_file.size / (1000 * 1000),))
            return HttpResponseRedirect(reverse("emp_upload_csv"))

        file_data = csv_file.read().decode("utf-8")

        lines = file_data.split("\n")

        # loop over the lines and save them in db. If error ,
        #  store as string and then display
        for line in lines:
            if line != "":
                fields = line.split(",")

                data_dict = dict()
                data_dict["emp_name"] = fields[0]
                data_dict["emp_username"] = fields[1]
                data_dict["emp_password"] = fields[2]
                data_dict["emp_designation"] = fields[3]
                data_dict["emp_address"] = fields[4]
                data_dict["company"] = fields[5]
                m = (data_dict["company"]).strip()

                try:
                    form = EventsForm(data_dict)
                    if data_dict.get('company') == request.session.get(
                            'org_name'):
                        org_names = Organization.objects.get(
                            company_name=request.session.get('org_name'))

                        org_employee_obj = Employee()
                        org_employee_obj.emp_name = data_dict["emp_name"]
                        org_employee_obj.emp_username = data_dict[
                            "emp_username"]
                        org_employee_obj.emp_password = data_dict[
                            "emp_password"]
                        org_employee_obj.emp_designation = data_dict[
                            "emp_designation"]
                        org_employee_obj.emp_address = data_dict["emp_address"]
                        org_employee_obj.company = org_names

                        org_employee_obj.save()
                except Exception as e:
                    logging.getLogger("error_logger").error(repr(e))
                    pass

    except Exception as e:
        logging.getLogger("error_logger").error(
            "Unable to upload file. " + repr(e))

        messages.error(request, "Unable to upload file. " + repr(e))

    return HttpResponseRedirect(reverse("emp_upload_csv"))


def add_survey(request):
    """
    adding multiple surveys
    """
    if request.method == "POST":
        if request.POST.get('sur_name') \
                and request.POST.get('sur_desc'):

            org_name = request.session.get('org_name')
            survey_obj1 = Survey()
            survey_obj1.survey_name = request.POST.get('sur_name')
            survey_obj1.description = request.POST.get('sur_desc')
            survey_obj1.company = Organization.objects.get(
                company_name=org_name)
            survey_obj1.date = datetime.datetime.now()
            survey_obj1.save()
            return redirect("add_survey")
        else:
            return redirect('index')
    return render(request, 'newsurvey/addsurveypage.html')


def getSuvey_list(request):
    """
    getting survey list
    """
    total_survey = Survey.objects.all()
    context = {'total_survey': total_survey}
    return HttpResponse(json.dumps(list(context)),
                        content_type="application/json")


def assign_survey(request):
    """
    assigning_survey
    :param request:
    :return:
    """
    survey_count = list()
    total_emplist = list()
    org_name = request.session.get('org_name')
    # org_obj = Organization.objects.get(company_name=org_name)
    total_survey = Survey.objects.filter(company__company_name=org_name)
    survey_count.append(total_survey)
    emp_list = Employee.objects.filter(company__company_name=org_name)

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
        start_date_str = request.POST.get('startdatepicker')
        end_date_str = request.POST.get('enddatepicker')

        start_date = datetime.datetime.strptime(start_date_str, '%m/%d/%Y')
        end_date = datetime.datetime.strptime(end_date_str, '%m/%d/%Y')

        emp_objs = list()
        for emp in emp_list:
            emp_objs.append(Employee.objects.get(emp_username=emp))

        survey_objs = list()
        for survey in surveys_list:
            survey_objs.append(Survey.objects.get(survey_name=survey))

        print("suvryes", surveys_list)
        print("emp", emp_list)

        for survey in survey_objs:
            for emp in emp_objs:
                survey_emp_map = SurveyEmployee(survey=survey,
                                                employee=emp,
                                                start_date=start_date,
                                                end_date=end_date)
                survey_emp_map.save()

    elif request.method == 'GET':
        print(request.POST.getlist('surveys'))
        print(request.POST.getlist('employees'))
    return redirect('index')


def add_questions(request):
    total_survey = Survey.objects.all()
    """
      csv extract
      """
    data = {}

    if "GET" == request.method:
        return render(request, 'newsurvey/addquestions.html', {
            'total_surveylist': total_survey}, data)
    # if not GET, then proceed
    try:
        print("enter try")

        csv_file = request.FILES["questionsv_file"]
        print("csv_key", csv_file)
        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'File is not CSV type')
            return HttpResponseRedirect(reverse("add_questions"))
        # if file is too large, return
        if csv_file.multiple_chunks():
            messages.error(request, "Uploaded file is too big (%.2f MB)." % (
            csv_file.size / (1000 * 1000),))
            return HttpResponseRedirect(reverse("add_questions"))

        file_data = csv_file.read().decode("utf-8")
        print("file data", file_data)

        lines = file_data.split("\n")

        # loop over the lines and save them in db. If error ,
        #  store as string and then display
        # qn_list = list()

        qn_survey = SurveyQuestion()
        try:
            survey_name = request.POST.get('dropdownid')
            print(survey_name)
            qn_survey.survey = Survey.objects.filter(
                survey_name=survey_name)[0]

        except Exception as e:
            print("No such Survey available.")
        for line in lines:
            if line != "":
                fields = line.split(":")    # separate fields on ':'
                print("fields", fields)
                print("filedsss", len(fields))

                data_dict = dict()
                data_dict["question_type"] = fields[0].split('"')[
                    1] if '"' in fields[0] else fields[0]
                data_dict["question"] = fields[1]
                data_dict["is_required"] = True if 'True' in fields[
                    2] else False
                if len(fields) == 4:
                    data_dict["choices"] = fields[3].split(
                        '"')[0] if '"' in fields[3] else fields[3]
                else:
                    data_dict["choices"] = None

                try:
                    org_question_obj = Question()
                    org_question_obj.Question_types.set(
                        data_dict.get("question_type"))
                    org_question_obj.question = data_dict["question"]
                    org_question_obj.is_required = data_dict["is_required"]
                    org_question_obj.choices.set = data_dict["choices"]

                    org_question_obj.save()
                    qn_survey.question.add(org_question_obj)

                except Exception as e:
                    logging.getLogger("error_logger").error(repr(e))
                    pass

            qn_survey.save()

    except Exception as e:
        logging.getLogger("error_logger").error(
            "Unable to upload file. " + repr(e))
        messages.error(request, "Unable to upload file. " + repr(e))

    return HttpResponseRedirect(reverse("add_questions"))


def emp_survey_assign(request):
    """
    View to render dashboard page for employee when employee logs in.
    """
    m = request.session['username']
    emp = Employee.objects.get(emp_username=m)
    emp_record = SurveyEmployee.objects.filter(employee=emp.id)
    Completed_survey = list()
    incomplete_survey = list()
    assign_survey = list()
    total_survey = list()
    status_check = False
    assign_surveycount1 = 0
    completed_surveylen = 0
    incomplete_surveylen = 0

    for survey in emp_record:
        # import pdb;
        # pdb.set_trace()
        survey_count = SurveyResponse.objects.filter(employee_id=emp.id,
                                                     survey_id=survey.survey_id
                                                     ).count()
        survey_submitted_count = SurveyEmployee.objects.filter(
            employee_id=emp.id,
            survey_id=survey.survey_id,
            submited_survey=True
        ).count()

        if survey_count:
            if survey_submitted_count:
                Completed_survey.append(survey)
            else:
                incomplete_survey.append(survey)
        else:
            assign_survey.append(survey)

        incomplete_surveylen = len(incomplete_survey)
        completed_surveylen = len(Completed_survey)
        print("completed survey", completed_surveylen)
        print("incomplete survey", incomplete_surveylen)
        assign_surveycount1 = len(assign_survey)

        status_check = SurveyResponse.objects.filter(
            survey_id=survey.survey_id, employee_id=emp.id)

    context = {
        'session': m,
        'total_survey': total_survey,
        'StatusCheck': status_check,
        'survey_list': emp_record,
        'completed_survey': Completed_survey,
        'incomplete_survey': incomplete_survey,
        'assign_survey': assign_surveycount1,
        'complete_count': completed_surveylen,
        'incomplete_count': incomplete_surveylen}

    return render(request, 'newsurvey/empdashboard.html', context)


def question_list(request, survey_id):
    """
    View to render the list of questions in a survey assigned to an employee.
    """
    m = request.session['username']

    unresponded_qns = SurveyResponse.objects.filter(survey__id=survey_id,
                                                    SaveStatus=False)

    if unresponded_qns:
        emp_record = SurveyResponse.objects.filter(
            survey__id=survey_id, SaveStatus=False).values(
            'question__id', 'question__question_type',
            'question__question', 'question__choices')
    else:
        emp_record = SurveyQuestion.objects.filter(
            survey__id=survey_id).values(
            'question__id', 'question__question_type',
            'question__question', 'question__choices')

    page = request.GET.get('page')
    paginator = Paginator(emp_record, 5)

    try:
        emp_record = paginator.page(page)
    except PageNotAnInteger:
        emp_record = paginator.page(1)
    except EmptyPage:
        emp_record = paginator.page(paginator.num_pages)

    for qn in emp_record:
        qn['question__choices'] = qn.get('question__choices').split(
            ",") if qn.get('question__choices') else None

    context = {'session': m,
               'survey_id': survey_id,
               'question_list': emp_record}

    return render(request, 'newsurvey/question_list.html', context)


def save(request, survey_id):
    """
    View to handle saving the survey in between. (without submitting)
    """
    m = request.session['username']
    emp = Employee.objects.get(emp_username=m)

    for name in request.POST:
        if name != "csrfmiddlewaretoken" and name != "submitform":

            if request.POST['submitform'] == "Submit":
                print("aaaa")
                emp = SurveyEmployee.objects.get(
                    employee_id=emp.id,
                    survey_id=Survey.objects.get(id=survey_id).id)
                emp.submited_survey = True
                emp.save()
                
            is_record = SurveyResponse.objects.filter(
                survey=Survey.objects.get(id=survey_id),
                employee=Employee.objects.get(id=emp.id),
                question=Question.objects.get(id=name))

            if not is_record:
                if request.POST[name]:
                    save_object = False
                    # survey_response_obj = SurveyResponse()
                    # survey_response_obj.survey = Survey.objects.get(
                    #     id=survey_id)
                    # survey_response_obj.employee = Employee.objects.get(
                    #     id=emp.id)
                    # survey_response_obj.question = Question.objects.get(
                    #     id=name)
                    # survey_response_obj.response = request.POST[name]
                    if request.POST['submitform'] == "Save" and \
                            request.POST[name] != '':
                        save_object = True
                    else:
                        save_object = False

                    survey_obj, created = SurveyResponse.objects.get_or_create(
                        survey=Survey.objects.get(id=survey_id),
                        employee=Employee.objects.get(id=emp.id),
                        question=Question.objects.get(id=name),
                        response=request.POST.get(name),
                        SaveStatus=save_object
                    )
                    # import pdb;pdb.set_trace()
                    if not created:
                        survey_obj.response = request.POST.get(name)
                        survey_obj.save()

    return redirect("emp_survey_assign")


def select_emp_action(request):
    """
    Select view to render for adding employees.
    """

    return render(request, 'newsurvey/emplist.html')


def redirect_to_emp_view(request):
    """
    Render the emp add view depending on selected option.
    :param request:
    :return:
    """
    selected_option = request.POST.get('radiobtn')

    if selected_option == 'Select_CSV':
        return render(request, 'newsurvey/emp_csv.html')

    elif selected_option == 'Fill_form':
        org_list = Organization.objects.all()
        return render(request, 'newsurvey/emp_form.html', {
            'org_total': org_list})


def render_emp_form(request):
    """
    render the view for adding single employee to the system.
    :param request:
    :return:
    """
    return render(request, 'newsurvey/emp_form.html')


def emp_form_save(request):
    """
    adding multiple surveys
    """
    if request.method == "POST":
            org_name = request.POST.get('OrgnisationName')
            empform_obj1 = Employee()
            empform_obj1.emp_name = request.POST.get('emp_name')
            empform_obj1.emp_username = request.POST.get('emp_username')
            empform_obj1.emp_password = request.POST.get('emp_password')
            empform_obj1.emp_designation = request.POST.get('emp_designation')
            empform_obj1.emp_address = request.POST.get('emp_address')
            empform_obj1.company = Organization.objects.get(
                company_name=org_name)
            empform_obj1.save()
            return redirect("index")
    else:
        return redirect('index')
