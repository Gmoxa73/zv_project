"""
URL configuration for MyProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path
from bd.views import address_list, raion_detail, device_detail, destination_page


urlpatterns = [
    path('admin/', admin.site.urls),
    path('addr/', address_list, name='address_list'),
    path('raions/<int:pk>/', raion_detail, name='raion_detail'),
    path('devices/<int:pk>/', device_detail, name='device_detail'),
    path('qust<int:addr_id>', destination_page, name='destination_page'),
]
