from django.urls import path
from .views import math_table

urlpatterns = [
    path('table/', math_table),
]