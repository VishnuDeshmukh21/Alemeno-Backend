from django.urls import path
from .views import analyze_strip, index

urlpatterns = [
   path('', index, name='index'),
    path('analyze/', analyze_strip, name='analyze_strip'),
]
