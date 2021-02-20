"""aggregator_django URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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

"""route urls to certain location so they can be handles by certain way"""
"""goes to URL admin, then logic in admin.site.urls handels the route further"""
urlpatterns = [

    path('admin/', admin.site.urls), # leave trailing slashes

    # aggregator part of the url was already proccessed- being choped off
    # therefore urls in app receive epmty string(matches home '')
    # Benefits of this system - aggregator_dev/ - to switch from live to development

    # path('aggregator/', include('aggregator.urls')),
    path('', include('aggregator.urls')), # to make it main landing page of project
]
