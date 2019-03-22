"""
Admin modules
"""
from django.contrib import admin
from .models import (Organization, org_Admin, Employee,
                     Survey, SurveyEmployee, SurveyQuestion, SurveyResponse,
                     Question)

admin.site.register(Organization)
admin.site.register(org_Admin)
admin.site.register(Employee)
admin.site.register(Survey)
admin.site.register(SurveyEmployee)
admin.site.register(SurveyQuestion)
admin.site.register(SurveyResponse)
admin.site.register(Question)
