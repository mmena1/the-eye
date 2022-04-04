from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', include('the_eye.urls')),
]
