
from django.shortcuts import render
from master.models import (Bdlreimbursement, Logbookheader, MasterEmployee, MasterBudget, Logbookbudget, LogbookLayer)
import datetime
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.db.models import Sum, Max
import uuid
from app.models import DocumentLogbook, IncrementIdBDL
from django.core.files.storage import FileSystemStorage


def formbdl(request):
    code_last = IncrementIdBDL.objects.last()
    print(code_last.doc_id)
    last_code = IncrementIdBDL.objects.aggregate(Max('doc_id'))
    code = code_last.doc_id
    print(code)
    new_code_int = int(code[7:12]) + 1
    print(new_code_int)
    doc_id = str(request.user)+ str(datetime.date.today().month) + str(datetime.date.today().day) + str(new_code_int)
    listbdl = Bdlreimbursement.objects.filter(doc_id=doc_id)
    data_employee = MasterEmployee.objects.get(emp_no=request.user)
    atasan1 = MasterEmployee.objects.get(emp_no=data_employee.approverid1)
    atasan2 = MasterEmployee.objects.get(emp_no=data_employee.approverid2)
    codebudget = MasterBudget.objects.filter(division_budget=data_employee.budget_code, fy='2021')
    logbook_budget = Logbookbudget.objects.filter(doc_id=doc_id)
    context = {
        'id':doc_id,
        'listbdl':listbdl,
        'dataemp':data_employee,
        'codebudget':codebudget,
        'atasanpertama':atasan1,
        'atasankedua':atasan2,
        'logbook_budget':logbook_budget,
    }
    return render(request,'logbook/bdl/list.html', context)


def bdl_save(request):
    if request.method!="POST":
        return HttpResponseRedirect(reverse("form-bdl"))
    else:
        ## ambil data dari response json template#
        doc_id = request.POST.get("id")
        print(doc_id)
        nik=request.POST.get("nik")
        print(nik)
        paid=request.POST.get("paid")
        norek = request.POST.get("norek")
        bankname = request.POST.get("bankname")
        nomor_police = request.POST.get("nomor_police")
        brand = request.POST.get("brand")
        type = request.POST.get("type")
        approver1 = request.POST.get("approver1")
        approver2 = request.POST.get("approver2")
        budgetcode = request.POST.get("codebudget")
        destinationfrom = request.POST.get("destinationfrom")
        destinationto = request.POST.get("destinationto")
        purpose = request.POST.get("purpose")
        date = request.POST.get("bdl_date")

        startkm = request.POST.get("startkm")
        endkm = request.POST.get("endkm")
        claimkm = request.POST.get("claimkm")
        currency = request.POST.get("currency")
        bdlperkm =request.POST.get("bdlperkm")
        parking  =request.POST.get("parking")
        bensin  =request.POST.get("bensin")
        tips  =request.POST.get("tips")
        toll =request.POST.get("toll")
        ## ambil data dari response json template#

        # untuk Model Bdlreimbursement #
        ## calculate setiap pengajuan tanggal 

        ## menghitung jumlah kilometer # km
        km =int(endkm) - int(startkm)

        totalkm = int(claimkm)

        ## km di * default level employee bdl per day
        bdlammount = int(totalkm) * int(bdlperkm)
        
        ## + all transaksi untuk bdl total dari setiap transaksi
        bdltotal = int(bdlammount) + (int(parking) + int(bensin) + int(toll) + int(tips))
        # untuk Model LogbookBudget #

        codebudget = budgetcode
        print(codebudget)
        ##dengan cara mengecek doc_id yang sama serta kode budget

        
        try:
            # untuk Model Bdlreimbursement #
            bdl_form_save=Bdlreimbursement(
            doc_id=doc_id, budget_code=budgetcode,
            bdldate=date, start_km=startkm,
            km=km,finish_km=endkm, curr=currency, bdl_perkm=bdlperkm,
            bdl_amount=bdlammount, bdl_total=bdltotal,destinationfrom=destinationfrom,
            destinationto = destinationto, purpose=purpose, parking=parking,
            toll = toll, policeno=nomor_police,carbrand=brand,cartype=type,
            tips=tips,bensin=bensin
            )
            bdl_form_save.save()
            # untuk Model Bdlreimbursement #
            

            
            # untuk Model LogbookBudget #
            ammount = ''
            
            ## create var empty
            
            cek =  Logbookbudget.objects.filter(doc_id=doc_id, budget_code=budgetcode).exists() ## mengechek terlebih dahulu doc_id & budget apakah sudah ada/sama atau belum
            if cek: ## jika true maka increment/jumlahkan field 'amt' dengan yang baru
                cariamt = Logbookbudget.objects.filter(doc_id=doc_id, budget_code=budgetcode).order_by('amt').last()# cari dulu dengan yang sama
                ketemuamt = cariamt.amt # masukin ke variable dulu
                ammount = float(ketemuamt) + float(bdltotal) # jika sama maka ## get ammount di jumlahkan dengan ammaount yang baru
                print(ammount)
                Logbookbudget.objects.filter(doc_id=doc_id,date_from=date,date_to=date,budget_code=budgetcode).update(amt=ammount) # save
                
            elif cek != True: # jika false maka buat lah row baru 
                listcodebudget = MasterBudget.objects.get(budget_number__contains=codebudget) # mengambil data dari MasterBudget
                
                logbookbudgetsave = Logbookbudget(
                    doc_id=doc_id,date_from=date,date_to=date,budget_code=budgetcode,
                gl_name=listcodebudget.gl_name,gl_no=listcodebudget.gl_no, div_code=listcodebudget.division_budget, curr=currency,amt=bdltotal,remark=codebudget+','+'BDL'+','+paid+','+date)
                  
                logbookbudgetsave.save() # save dan masukan datanya
                print('ini elif :'  + listcodebudget.gl_name) ## cek apakah masuk
            else :
                listcodebudget = MasterBudget.objects.get(budget_number__contains=codebudget) ## lainya dari kondisi di atas
                ## membuat benar benar baru 
                Logbookbudget.objects.get_or_create(
                    doc_id=doc_id,date_from=date,date_to=date,budget_code=budgetcode,
                gl_name=listcodebudget.gl_name,gl_no=listcodebudget.gl_no, div_code=listcodebudget.division_budget, curr=currency,amt=bdltotal,remark=codebudget+','+'BDL'+','+paid+','+date)    
                print( 'ini else :'  + listcodebudget.gl_name)
            messages.success(request, "Successfully Applied for BDL") ## mengembalikan pesan error ke UI
            return HttpResponseRedirect(reverse("app:form-bdl")) ## kembali ke from-bdl 
        except:
            messages.error(request, "Failed To Apply for BDL")
            return HttpResponseRedirect(reverse("app:form-bdl"))




def bdl_draft_to(request):
    data_employee = MasterEmployee.objects.get(emp_no=request.user)
    atasan1 = MasterEmployee.objects.get(emp_no=data_employee.approverid1)
    atasan2 = MasterEmployee.objects.get(emp_no=data_employee.approverid2)
    doc_id = request.POST.get('id')
    print(doc_id)
    remark = request.POST.get('bdsremark')
    cariamt = Logbookbudget.objects.filter(doc_id=doc_id).aggregate(Sum('amt'))
    print(cariamt)
    layer = LogbookLayer.objects.filter(doc_type=1).values('emp_no')
    print(layer)
    datetimenow = datetime.datetime.now()
    total_payment_idr = cariamt['amt__sum']
    print(total_payment_idr)

    app = ''
    for app in layer :
        app = layer
    

    app3 = app[0]['emp_no']
    app4 = layer[1]['emp_no']
    app5 = layer[2]['emp_no']
    app6 = layer[3]['emp_no']
    app7 = layer[4]['emp_no']
    app8 = layer[5]['emp_no']
    app9 = layer[6]['emp_no']
    app10 = layer[7]['emp_no']
    
    try :
        createdrafttoheader = Logbookheader(doc_id=doc_id, 
        doc_type=1,
        userid=str(request.user),
        emp_no=str(request.user),
        doc_remark=remark +","+"BDL FROM:" + datetimenow.strftime('%Y-%m-%d'),
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
        approver_5 = app5,
        approver_6 = app6,
        approver_7 = app7,
        approver_8 = app8,
        approver_9 = app9,
        approver_10 = app10,
    
            )
        createdrafttoheader.save()
        saveincrement = IncrementIdBDL(doc_id=doc_id, nik=str(request.user), name_doc='BDL')
        saveincrement.save()
        messages.success(request, "Successfully Applied for BDL")
        return HttpResponseRedirect(reverse("app:bdl_draft"))
    except:
        messages.error(request, "Failed To Apply for BDL")
        return HttpResponseRedirect(reverse("app:form-bdl"))


def bdl_draft(request):
    bdldraft = Logbookheader.objects.filter(emp_no=request.user, status='draft')
    context = {
        'bdldraft':bdldraft,
    }
    return render(request,'logbook/bdl/draft.html', context)

def sendtoapprover(request, doc_id):
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

def mydocumentbdl(request):
    layer = LogbookLayer.objects.filter(doc_type=1).values('alias_name')
    bdldraft = Logbookheader.objects.filter(emp_no=request.user, status='Sending', doc_type=1)

    context = {
        'bdldraft':bdldraft,
        'layer':layer,
    }
    return render(request, 'logbook/bdl/mydocument.html', context)


def deletebdl(request, doc_id):
    id = doc_id 
    try:
        Bdlreimbursement.objects.filter(doc_id=id).delete()
        Logbookbudget.objects.filter(doc_id=id).delete()
        Logbookheader.objects.filter(doc_id=id).delete()
        messages.success(request, "Successfully To Delete   " + str(id))
        return HttpResponseRedirect(reverse("app:bdl_draft"))
    except:
        messages.error(request, "Failed To Delete   " + str(id))
        return HttpResponseRedirect(reverse("app:bdl_darft"))


def editbdl(request, doc_id):
    listbdl = Bdlreimbursement.objects.filter(doc_id=doc_id)
    data_employee = MasterEmployee.objects.get(emp_no=request.user)
    atasan1 = MasterEmployee.objects.get(emp_no=data_employee.approverid1)
    atasan2 = MasterEmployee.objects.get(emp_no=data_employee.approverid2)
    codebudget = MasterBudget.objects.filter(division_budget=data_employee.budget_code, fy='2021')
    logbook_budget = Logbookbudget.objects.filter(doc_id=doc_id)
    context = {
        'id':doc_id,
        'listbdl':listbdl,
        'dataemp':data_employee,
        'codebudget':codebudget,
        'atasanpertama':atasan1,
        'atasankedua':atasan2,
        'logbook_budget':logbook_budget,
    }
    return render(request,'logbook/bdl/edit.html', context)


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