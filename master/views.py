from django.http import response
from django.shortcuts import render
from rest_framework import serializers, permissions, generics, filters
from rest_framework.decorators import api_view
from master.serializers import DetailLogbookSerializer
from master.models import Bdlreimbursement
from django_filters.rest_framework import DjangoFilterBackend
from todos.pagination import CustomPageNumberPagination
from django.http import JsonResponse
import pyodbc
from master.models import Bdlreimbursement


# Create your views here.
class BdlListAPIView(generics.ListAPIView):
    serializer_class = DetailLogbookSerializer
    permission_classes=(permissions.IsAuthenticated,)
    queryset = Bdlreimbursement.objects.all()


class BdlReimbustmentAPIView(generics.ListCreateAPIView):
    serializer_class = DetailLogbookSerializer
    pagination_class = CustomPageNumberPagination
    permission_classes=(permissions.IsAuthenticated,)
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    filterset_fields = ['id', 'doc_id', 'bdl_total',]
    search_fields = ['id', 'doc_id', 'bdl_total',]
    ordering_fields = ['id', 'doc_id', 'bdl_total',]

    def perform_create(self, serializer):
        return serializer.save()

    def get_queryset(self):
        return Bdlreimbursement.objects.filter(doc_id=self.request.data['doc_id'])


class TodosDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = DetailLogbookSerializer
    permission_classes=(permissions.IsAuthenticated,)
    lookup_field = "id"

    def get_queryset(self):
        return Bdlreimbursement.objects.filter(owner=self.request.user)



def main(request):
    return render(request,'dashboard.html')