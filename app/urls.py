# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from app import views
from app.logbook.views_bdl import (deletebdl, editbdl, formbdl, 
bdl_save,bdl_draft_to,bdl_draft, mydocumentbdl, uploaddocument,
sendtoapprover, deletebdl, editbdl, viewdocument)

from app.logbook.views_medical import (deletemedical, deletemedical, editmedical, medical_draft_to, 
medical_save,medical_draft, formmedical, mydocumentmedical, sendtoapprovermedical, uploaddocument,  viewdocument, )

from app.logbook.views_entertainment import ( formentertainment, 
entertainment_save,enter_draft_to,enter_draft, mydocumententer, uploaddocument,
sendtoapproverenter, deleteenter, editenter, viewdocument)

from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    # The home page
    path('', views.index, name='home'),
    # The Logbook BDL 
    path('form-bdl', formbdl, name='form-bdl'),
    path('save-bdl', bdl_save, name='save-bdl'),
    path('bdl_draft_to', bdl_draft_to, name='bdl_draft_to'),
    path('bdl_draft', bdl_draft, name='bdl_draft'),
    path('send_to_approver/<str:doc_id>/', sendtoapprover, name='send_to_approver'),
    path('bdl-mydocument', mydocumentbdl, name='bdl-mydocument'),
    path('delete-bdl/<str:doc_id>', deletebdl, name='delete-bdl'),
    path('edit-bdl/<str:doc_id>', editbdl, name='edit-bdl'),
    path('view-bdl/<str:doc_id>', viewdocument, name='view-bdl'),
    # The Logbook BDL #


    # the Logbook Medical #

    path('form-medical', formmedical, name='form-medical'),
    path('medical-save', medical_save, name='medical-save'),
    path('medical_draft_to', medical_draft_to, name='medical_draft_to'),
    path('medical_draft', medical_draft, name='medical_draft'),
    path('send_to_approver_medical/<str:doc_id>/', sendtoapprovermedical, name='send_to_approver_medical'),
    path('medical-mydocument', mydocumentmedical, name='medical-mydocument'),
    path('delete-medical/<str:doc_id>', deletemedical, name='delete-medical'),
    path('edit-medical/<str:doc_id>', editmedical, name='edit-medical'),
    path('view-bdl/<str:doc_id>', viewdocument, name='view-bdl'),

    # the Logbook Medical #

    # the Logbook Entertaiment #

    path('form-entertaiment', formentertainment, name='form-entertaiment'),
    path('save-entertainment', entertainment_save, name='save-entertainment'),
    path('enter_draft_to', enter_draft_to, name='enter_draft_to'),
    path('enter_draft', enter_draft, name='enter_draft'),
    path('send_to_approver_enter/<str:doc_id>/', sendtoapproverenter, name='send_to_approver_enter'),
    path('enter-mydocument', mydocumententer, name='enter-mydocument'),
    path('delete-enter/<str:doc_id>', deleteenter, name='delete-enter'),
    path('edit-enter/<str:doc_id>', editenter, name='edit-enter'),
    path('view-bdl/<str:doc_id>', viewdocument, name='view-bdl'),
   
    # the Logbook Entertainment #

    


     path('upload-document/<str:doc_id>/', uploaddocument, name='upload-document'),
    
    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
