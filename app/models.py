# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields import CharField

# Create your models here.

class IncrementIdBDL(models.Model):
    doc_id = models.CharField(max_length=20, blank=True, null=True)
    nik = models.CharField(max_length=6, blank=True, null=True)
    name_doc = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

class DocumentLogbook(models.Model):
    doc_id = models.CharField(max_length=20, blank=True, null=True)
    nik = models.CharField(max_length=6, blank=True, null=True)
    docreceipt = models.ImageField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)


    @property
    def imageURL(self):
        try:
            url = self.docreceipt.url
        except :
            url = ''
        return url




    