"""advancesurvey URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
# start mailing scheduler every time the server starts running
from newsurvey.email_schedular import ScheduleSendEmail

urlpatterns = [
    path('admin/', admin.site.urls),
    path('newsurvey/', include('newsurvey.urls')),
    path('', RedirectView.as_view(url='/newsurvey/login'))

]

ScheduleSendEmail.get_mailee_data()
