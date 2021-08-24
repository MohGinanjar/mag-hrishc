from django.urls import path
from rest_framework import views

from master.views import main

from master.views import BdlListAPIView, BdlReimbustmentAPIView



urlpatterns = [
    
    path('bdl-detail-create', BdlReimbustmentAPIView.as_view(), name='bdl-detail-create'),
    path('main',  main, name='main')
    
]