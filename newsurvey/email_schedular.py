import time
import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
from django.core.mail import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from .models import SurveyEmployee

sched = BlockingScheduler()


class ScheduleSendEmail(object):

    @staticmethod
    @sched.scheduled_job('cron', hour=12)
    def get_mailee_data():
        """
        Get the employees data to whom mails to be sent.
        :return:
        """
        print("In mailer")
        shcedule_email_obj = ScheduleSendEmail()
        shcedule_email_obj.__get_today_start_date()
        shcedule_email_obj.__get_today_end_date()
        shcedule_email_obj.__get_one_day_before_start()
        shcedule_email_obj.__get_one_day_before_end()

    def __send_email(self, mailee, subject, msg_body):
        """
        Send an email to the employee with survey link.
        """
        try:
            email = EmailMessage(
                subject=subject,
                body=msg_body,
                to=[mailee])
            email.send()

        except Exception as e:
            print(e)
            return False
        else:
            return True

    def __get_today_start_date(self):
        """
        Send mail to employees having survey start date today.
        :return:
        """
        mailee_list = SurveyEmployee.objects.filter(
            start_date=datetime.datetime.today()).values(
            'employee', 'survey__survey_name', 'survey__company__company_name',
            'start_date', 'end_date', 'employee__emp_address')

        for mailee in mailee_list:
            email_address = mailee.get('employee__emp_address')
            survey_list = mailee.get('survey__survey_name')
            org_name = mailee.get('survey__company__company_name')

            body = "Hi,\n" + "You are selected for " + str(
                len(survey_list)) + " survey(s) for organization: " + (
                org_name) + \
                "\nLink for logging in: http://127.0.0.1:8000/newsurvey/login"

            mailing_status = self.__send_email(email_address,
                                               "Survey starting today",
                                               body)

            if mailing_status:
                print("mailing successful")
            else:
                print("mailing unsuccessful")

    def __get_today_end_date(self):
        """
        Send mail to employees having survey end date today.
        :return:
        """
        mailee_list = SurveyEmployee.objects.filter(
            end_date=datetime.datetime.today()).values(
            'employee', 'survey__survey_name', 'survey__company__company_name',
            'start_date', 'end_date', 'employee__emp_address')

        for mailee in mailee_list:
            email_address = mailee.get('employee__emp_address')
            survey_list = mailee.get('survey__survey_name')
            org_name = mailee.get('survey__company__company_name')

            body = "Hi,\n" + "You are selected for " + str(
                len(survey_list)) + " survey(s) for organization: " + (
                       org_name) + \
                "\nLink for logging in: http://127.0.0.1:8000/newsurvey/login"

            mailing_status = self.__send_email(email_address,
                                               "Survey starting today",
                                               body)

            if mailing_status:
                print("mailing successful")
            else:
                print("mailing unsuccessful")

    def __get_one_day_before_start(self):
        """
        Send mail to employees having survey end day after today.
        :return:
        """
        mailee_list = SurveyEmployee.objects.filter(
            start_date=datetime.datetime.today() + datetime.timedelta(days=2)
        ).values(
            'employee', 'survey__survey_name', 'survey__company__company_name',
            'start_date', 'end_date', 'employee__emp_address')

        for mailee in mailee_list:
            email_address = mailee.get('employee__emp_address')
            survey_list = mailee.get('survey__survey_name')
            org_name = mailee.get('survey__company__company_name')

            body = "Hi,\n" + "You are selected for " + str(
                len(survey_list)) + " survey(s) for organization: " + (
                       org_name) + \
                "\nLink for logging in: http://127.0.0.1:8000/newsurvey/login"

            mailing_status = self.__send_email(email_address,
                                               "Survey starting today",
                                               body)

            if mailing_status:
                print("mailing successful")
            else:
                print("mailing unsuccessful")

    def __get_one_day_before_end(self):
        """
        Send mail to employees having survey end day after today.
        :return:
        """
        mailee_list = SurveyEmployee.objects.filter(
            end_date=datetime.datetime.today() + datetime.timedelta(days=2)
        ).values(
            'employee', 'survey__survey_name', 'survey__company__company_name',
            'start_date', 'end_date', 'employee__emp_address')

        for mailee in mailee_list:
            email_address = mailee.get('employee__emp_address')
            survey_list = mailee.get('survey__survey_name')
            org_name = mailee.get('survey__company__company_name')

            body = "Hi,\n" + "You are selected for " + str(
                len(survey_list)) + " survey(s) for organization: " + (
                       org_name) + \
                "\nLink for logging in: http://127.0.0.1:8000/newsurvey/login"

            mailing_status = self.__send_email(email_address,
                                               "Survey starting today",
                                               body)

            if mailing_status:
                print("mailing successful")
            else:
                print("mailing unsuccessful")

