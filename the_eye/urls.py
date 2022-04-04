from django.urls import re_path
from rest_framework.urlpatterns import format_suffix_patterns
from the_eye import views

urlpatterns = [
    re_path(r'^events/?$', views.EventList.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
