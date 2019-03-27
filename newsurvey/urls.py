"""
survey urls mapping
"""
from . import views
from django.urls import path

urlpatterns = [
    path('index/', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('add_org/', views.add_org, name='add_org'),
    path('getorgdata/', views.getorgdata, name='getorgdata'),
    path('admin_register/', views.admin_register,name='admin_register'),
    path('upload_csv/', views.select_emp_action, name='upload_csv'),
    path('Add_Survey/', views.Add_Survey, name='Add_Survey'),
    path('getSuvey_list/', views.getSuvey_list, name='getSuvey_list'),
    path('Assign_Survey/', views.Assign_Survey, name='Assign_Survey'),
    path('deleteorg/', views.delete_org, name='delete_org'),
    path('store_assigned_surveys/', views.store_assigned_surveys, name='store_assigned_surveys'),
    path('add_questions/', views.add_questions, name='add_questions'),
    path('emp_survey_assign/', views.emp_survey_assign, name='emp_survey_assign'),
    path('que_list/<int:survey_id>', views.question_list, name='que_list'),
    path('save/<int:survey_id>', views.save, name='save'),
    path('emp_csv/', views.select_emp_action, name='emp_upload_csv'),
    path('emp_form/', views.render_emp_form, name='emp_form'),
    path('redirect_to_view', views.redirect_to_emp_view, name='redirect_emp'),
    path('emp_form_save/', views.emp_form_save, name='emp_form_save')

]
