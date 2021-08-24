
from django.shortcuts import render
from master.models import (Bdlreimbursement, Logbookheader, MasterEmployee, MasterBudget, Logbookbudget, LogbookLayer, MasterFamily, Medicalreimbursement)
import datetime
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.db.models import Sum, Max
import uuid
from app.models import DocumentLogbook, IncrementIdBDL
from django.core.files.storage import FileSystemStorage


def formmedical(request):
    code_last = IncrementIdBDL.objects.last()
    last_code = IncrementIdBDL.objects.aggregate(Max('doc_id'))
    code = code_last.doc_id
    new_code_int = int(code[7:12]) + 1
    doc_id = str(request.user)+ str(datetime.date.today().month) + str(datetime.date.today().day) + str(new_code_int)
    listmedical = Medicalreimbursement.objects.filter(doc_id=doc_id)
    data_employee = MasterEmployee.objects.get(emp_no=request.user)
    atasan1 = MasterEmployee.objects.get(emp_no=data_employee.approverid1)
    atasan2 = MasterEmployee.objects.get(emp_no=data_employee.approverid2)
    codebudget = MasterBudget.objects.filter(division_budget=data_employee.budget_code, fy='2021')
    logbook_budget = Logbookbudget.objects.filter(doc_id=doc_id)
    family = MasterFamily.objects.filter(emp_no=request.user)
    context = {
        'id':doc_id,
        'listmedical':listmedical,
        'dataemp':data_employee,
        'codebudget':codebudget,
        'atasanpertama':atasan1,
        'atasankedua':atasan2,
        'logbook_budget':logbook_budget,
        'family':family,
    }
    return render(request,'logbook/medical/list.html', context)


def medical_save(request):
    if request.method!="POST":
        return HttpResponseRedirect(reverse("form-medical"))
    else:
        ## ambil data dari response json template#
        doc_id = request.POST.get("id")
        nik=request.POST.get("nik")
        paid=request.POST.get("paid")
        norek = request.POST.get("norek")
        bankname = request.POST.get("bankname")
        type = request.POST.get("type")
        approver1 = request.POST.get("approver1")
        approver2 = request.POST.get("approver2")
        budgetcode = request.POST.get("codebudget")
        date = request.POST.get("bdl_date")
        currency = request.POST.get("currency")
        familys =request.POST.get("familys")
        print(familys)
        diagnosa  =request.POST.get("diagnosa")
        ammount  =request.POST.get("ammount")

       
        namefamily = ''
        relation = ''
        if familys == "self":
            name = MasterEmployee.objects.get(emp_no = request.user)
            namefamily = name.emp_name
            relation = 'S'
        else :    
            name = MasterFamily.objects.get(id=familys)
            namefamily = name.fam_name
            relation = name.relation

        ## ambil data dari response json template#

        # untuk Model Bdlreimbursement #
        ## calculate setiap pengajuan tanggal 

        ## menghitung jumlah kilometer # km
        # km =int(endkm) - int(startkm)

        # totalkm = int(claimkm)

        # ## km di * default level employee bdl per day
        # bdlammount = int(totalkm) * int(bdlperkm)
        
        ## + all transaksi untuk bdl total dari setiap transaksi
        # bdltotal = int(bdlammount) + (int(parking) + int(bensin) + int(toll) + int(tips))
        # # untuk Model LogbookBudget #

        # codebudget = budgetcode
        # print(codebudget)
        ##dengan cara mengecek doc_id yang sama serta kode budget

        
        try:
            # untuk Model Bdlreimbursement #
            bdl_form_save=Medicalreimbursement(
            doc_id=doc_id, status='draft',
            receipt_dt=date, curr=currency,
            type=type,emp_no=nik,amount=ammount,fam_name=namefamily,relation=relation,diagnosa=diagnosa,
            
            )
            bdl_form_save.save()
            messages.success(request, "Successfully Applied for Medical") ## mengembalikan pesan error ke UI
            return HttpResponseRedirect(reverse("app:form-medical")) ## kembali ke from-bdl 
        except:
            messages.error(request, "Failed To Apply for Medical")
            return HttpResponseRedirect(reverse("app:form-medical"))




def medical_draft_to(request):
    data_employee = MasterEmployee.objects.get(emp_no=request.user)
    atasan1 = MasterEmployee.objects.get(emp_no=data_employee.approverid1)
    atasan2 = MasterEmployee.objects.get(emp_no=data_employee.approverid2)
    doc_id = request.POST.get('id')
    print(doc_id)
    remark = request.POST.get('bdsremark')
    cariamt = Medicalreimbursement.objects.filter(doc_id=doc_id).aggregate(Sum('amount'))
    print(cariamt)
    layer = LogbookLayer.objects.filter(doc_type=8).values('emp_no')
    print(layer)
    datetimenow = datetime.datetime.now()
    total_payment_idr = cariamt['amount__sum']
    print(total_payment_idr)

    app = ''
    for app in layer :
        app = layer
    

    app3 = app[0]['emp_no']
    app4 = layer[1]['emp_no']
    
    try :
        createdrafttoheader = Logbookheader(doc_id=doc_id, 
        doc_type=8,
        userid=str(request.user),
        emp_no=str(request.user),
        doc_remark=remark +","+"Medical FROM:" + datetimenow.strftime('%Y-%m-%d'),
        doc_date= datetimenow.strftime('%Y-%m-%d %H:%M:%S'),
       
        current_doc_sts = 'HRD',
        status = 'draft',
        bank_name = 'BANK CENTRAL ASIA',
        bank_no = data_employee.bank_acct,
        name_payment = data_employee.emp_name,
        total_payment_idr = total_payment_idr,
        total_payment_usd = 0.0,
        total_payment_ypn = 0.0,
        total_payment_bath = 0.0,
        total_payment_myr = 0.0,
        total_payment_sgd = 0.0,
        total_payment_euro = 0.0,

        act_state1 = 'NON',
        act_state2 = 'NON',
        act_state3 = 'NON',
        act_state4 = 'NON',
        act_state5 = 'NON',
        act_state6 = 'NON',
        act_state7 = 'NON',
        act_state8 = 'NON',
        act_state9 = 'NON',
        act_state10 = 'NON',


        approver_3 = app3,
        approver_4 = app4,
    
            )
        createdrafttoheader.save()
        saveincrement = IncrementIdBDL(doc_id=doc_id, nik=str(request.user), name_doc='Medical')
        saveincrement.save()
        messages.success(request, "Successfully Applied for Medical")
        return HttpResponseRedirect(reverse("app:medical_draft"))
    except:
        messages.error(request, "Failed To Apply for Medical")
        return HttpResponseRedirect(reverse("app:form-medical"))


def medical_draft(request):
    bdldraft = Logbookheader.objects.filter(emp_no=request.user, status='draft', doc_type=8)
    context = {
        'bdldraft':bdldraft,
    }
    return render(request,'logbook/medical/draft.html', context)

def sendtoapprovermedical(request, doc_id):
    id=doc_id
    print(id)
    data_employee = MasterEmployee.objects.get(emp_no=request.user)
    ## TODO : set sendemail , ambil data dari masteremployee or useraccount 'email'
    try:
        ## here sendemail 
        Logbookheader.objects.filter(doc_id = id).update(approver_1=data_employee.approverid1,approver_2=data_employee.approverid2, status='Sending')

        messages.success(request, "Successfully Applied To Superior")
        return HttpResponseRedirect(reverse("app:bdl-mydocument"))
    except:
        messages.error(request, "Failed To Apply To Superior")
        return HttpResponseRedirect(reverse("app:bdl-draft"))

def mydocumentmedical(request):
    layer = LogbookLayer.objects.filter(doc_type=8).values('alias_name')
    bdldraft = Logbookheader.objects.filter(emp_no=request.user, status='Sending', doc_type=8)

    context = {
        'bdldraft':bdldraft,
        'layer':layer,
    }
    return render(request, 'logbook/medical/mydocument.html', context)


def deletemedical(request, doc_id):
    id = doc_id 
    try:
        Medicalreimbursement.objects.filter(doc_id=id).delete()
        Logbookbudget.objects.filter(doc_id=id).delete()
        Logbookheader.objects.filter(doc_id=id).delete()
        messages.success(request, "Successfully To Delete   " + str(id))
        return HttpResponseRedirect(reverse("app:bdl_draft"))
    except:
        messages.error(request, "Failed To Delete   " + str(id))
        return HttpResponseRedirect(reverse("app:bdl_darft"))


def editmedical(request, doc_id):
    listmedical = Medicalreimbursement.objects.filter(doc_id=doc_id)
    data_employee = MasterEmployee.objects.get(emp_no=request.user)
    atasan1 = MasterEmployee.objects.get(emp_no=data_employee.approverid1)
    atasan2 = MasterEmployee.objects.get(emp_no=data_employee.approverid2)
    codebudget = MasterBudget.objects.filter(division_budget=data_employee.budget_code, fy='2021')
    context = {
        'id':doc_id,
        'listmedical':listmedical,
        'dataemp':data_employee,
        'codebudget':codebudget,
        'atasanpertama':atasan1,
        'atasankedua':atasan2,
        
    }
    return render(request,'logbook/medical/edit.html', context)


def uploaddocument(request, doc_id):
    if request.method == 'POST':
        uploded_files = request.FILES.getlist('documentes')
        
    try:
        for images in uploded_files:
            document = DocumentLogbook.objects.create(
                nik = request.user,
                docreceipt = images,
                doc_id = doc_id,
            )

        messages.success(request, "Successfully Upload Image")
        return HttpResponseRedirect(reverse("app:bdl_draft"))
    except:
        messages.error(request, "Failed Upload image")
        return HttpResponseRedirect(reverse("app:bdl_draft"))

    
        

def viewdocument(request, doc_id):
    documents = DocumentLogbook.objects.filter(doc_id=doc_id)
    context = {
        'documents':documents
    }
    return render(request, 'logbook/bdl/view.html', context)