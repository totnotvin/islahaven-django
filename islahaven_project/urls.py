"""
URL configuration for islahaven_project project.

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
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('rooms/', views.rooms, name='rooms'),
    path('ferry/', views.ferry, name='ferry'),
    path('book-ferry/', views.book_ferry, name='book_ferry'),
    path('tickets/', views.tickets, name='tickets'),
    path('events/', views.events, name='events'),
    path('login/', views.login, name='login'),
    path('booking-view/', views.booking_view, name='booking-view'),
    path('booking-detail/<int:booking_id>/', views.booking_detail, name='booking_detail'),
    path('dashboard/', views.dashboard, name='dashboard'),
]
