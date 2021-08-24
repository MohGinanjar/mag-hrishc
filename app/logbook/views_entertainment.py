
from django.shortcuts import render
from master.models import (Bdlreimbursement, Entertainment, Logbookheader, MasterEmployee, MasterBudget, Logbookbudget, LogbookLayer)
import datetime
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.db.models import Sum, Max
import uuid
from app.models import DocumentLogbook, IncrementIdBDL
from django.core.files.storage import FileSystemStorage


def formentertainment(request):
    code_last = IncrementIdBDL.objects.last()
    print(code_last.doc_id)
    last_code = IncrementIdBDL.objects.aggregate(Max('doc_id'))
    code = code_last.doc_id
    print(code)
    new_code_int = int(code[7:12]) + 1
    print(new_code_int)
    doc_id = str(request.user)+ str(datetime.date.today().month) + str(datetime.date.today().day) + str(new_code_int)
    listenter = Entertainment.objects.filter(doc_id=doc_id)
    data_employee = MasterEmployee.objects.get(emp_no=request.user)
    atasan1 = MasterEmployee.objects.get(emp_no=data_employee.approverid1)
    atasan2 = MasterEmployee.objects.get(emp_no=data_employee.approverid2)
    codebudget = MasterBudget.objects.filter(division_budget=data_employee.budget_code, fy='2021')
    logbook_budget = Logbookbudget.objects.filter(doc_id=doc_id)
    context = {
        'id':doc_id,
        'listenter':listenter,
        'dataemp':data_employee,
        'codebudget':codebudget,
        'atasanpertama':atasan1,
        'atasankedua':atasan2,
        'logbook_budget':logbook_budget,
    }
    return render(request,'logbook/entertainment/list.html', context)


def entertainment_save(request):
    if request.method!="POST":
        return HttpResponseRedirect(reverse("form-entertaiment"))
    else:
        ## ambil data dari response json template#
        doc_id = request.POST.get("id")
        print(doc_id)
        nik=request.POST.get("nik")
        print(nik)
        paid=request.POST.get("paid")
        currency = request.POST.get("currency")
        budgetcode = request.POST.get("codebudget")
        date = request.POST.get("enter_date")
        ammount = request.POST.get("ammount")
        customername = request.POST.get("customername")
        position = request.POST.get("position")
        company = request.POST.get("company")
        kindofbusines =request.POST.get("kindofbusines")
        
        
        
        
       
        ## ambil data dari response json template#

        # untuk Model Entertainment #
        ## calculate setiap pengajuan tanggal 

        # untuk Model LogbookBudget #

        codebudget = budgetcode
        print(codebudget)

        if codebudget == 'Open this select budget':
            messages.error(request, "Please Choose Code Budget")
            return HttpResponseRedirect(reverse("app:form-entertaiment"))
        else:
        ##dengan cara mengecek doc_id yang sama serta kode budget

        
            try:
                # untuk Model Bdlreimbursement #
                bdl_form_save=Entertainment(
                doc_id=doc_id, budget_code=budgetcode,
                remark=kindofbusines,ent_dt=date,customer_name=customername,customer_position=position,customer_company=company
                )
                bdl_form_save.save()
                # untuk Model Bdlreimbursement #
                

                
                # untuk Model LogbookBudget #
                
                ## create var empty
                
                cek =  Logbookbudget.objects.filter(doc_id=doc_id, budget_code=budgetcode).exists() ## mengechek terlebih dahulu doc_id & budget apakah sudah ada/sama atau belum
                if cek: ## jika true maka increment/jumlahkan field 'amt' dengan yang baru
                    cariamt = Logbookbudget.objects.filter(doc_id=doc_id, budget_code=budgetcode).order_by('amt').last()# cari dulu dengan yang sama
                    ketemuamt = cariamt.amt # masukin ke variable dulu
                    ammount = float(ketemuamt) + float(ammount) # jika sama maka ## get ammount di jumlahkan dengan ammaount yang baru
                    print(ammount)
                    Logbookbudget.objects.filter(doc_id=doc_id,date_from=date,date_to=date,budget_code=budgetcode).update(amt=ammount) # save
                    
                elif cek != True: # jika false maka buat lah row baru 
                    listcodebudget = MasterBudget.objects.get(budget_number__contains=codebudget) # mengambil data dari MasterBudget
                    
                    logbookbudgetsave = Logbookbudget(
                        doc_id=doc_id,date_from=date,date_to=date,budget_code=budgetcode,
                    gl_name=listcodebudget.gl_name,gl_no=listcodebudget.gl_no, div_code=listcodebudget.division_budget, curr=currency,amt=ammount,remark=codebudget+','+'ENTERTAINMENT'+','+paid+','+date)
                    
                    logbookbudgetsave.save() # save dan masukan datanya
                    print('ini elif :'  + listcodebudget.gl_name) ## cek apakah masuk
                else :
                    listcodebudget = MasterBudget.objects.get(budget_number__contains=codebudget) ## lainya dari kondisi di atas
                    ## membuat benar benar baru 
                    Logbookbudget.objects.get_or_create(
                        doc_id=doc_id,date_from=date,date_to=date,budget_code=budgetcode,
                    gl_name=listcodebudget.gl_name,gl_no=listcodebudget.gl_no, div_code=listcodebudget.division_budget, curr=currency,amt=ammount,remark=codebudget+','+'ENTERTAINMENT'+','+paid+','+date)    
                    print( 'ini else :'  + listcodebudget.gl_name)
                messages.success(request, "Successfully Applied for Entertainment") ## mengembalikan pesan error ke UI
                return HttpResponseRedirect(reverse("app:form-entertaiment")) ## kembali ke from-bdl 
            except:
                messages.error(request, "Failed To Apply for Entertainment")
                return HttpResponseRedirect(reverse("app:form-entertaiment"))




def enter_draft_to(request):
    data_employee = MasterEmployee.objects.get(emp_no=request.user)
    atasan1 = MasterEmployee.objects.get(emp_no=data_employee.approverid1)
    atasan2 = MasterEmployee.objects.get(emp_no=data_employee.approverid2)
    doc_id = request.POST.get('id')
    print(doc_id)
    remark = request.POST.get('bdsremark')
    cariamt = Logbookbudget.objects.filter(doc_id=doc_id).aggregate(Sum('amt'))
    print(cariamt)
    layer = LogbookLayer.objects.filter(doc_type=2).values('emp_no')
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
    
    
    try :
        createdrafttoheader = Logbookheader(doc_id=doc_id, 
        doc_type=2,
        userid=str(request.user),
        emp_no=str(request.user),
        doc_remark=remark +","+"Entertainment FROM:" + datetimenow.strftime('%Y-%m-%d'),
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
     
    
            )
        createdrafttoheader.save()
        saveincrement = IncrementIdBDL(doc_id=doc_id, nik=str(request.user), name_doc='Entertainment')
        saveincrement.save()
        messages.success(request, "Successfully Applied for Entertainment")
        return HttpResponseRedirect(reverse("app:enter_draft"))
    except:
        messages.error(request, "Failed To Apply for Entertainment")
        return HttpResponseRedirect(reverse("app:enter_draft"))


def enter_draft(request):
    bdldraft = Logbookheader.objects.filter(emp_no=request.user, status='draft' ,doc_type=2)
    context = {
        'bdldraft':bdldraft,
    }
    return render(request,'logbook/entertainment/draft.html', context)

def sendtoapproverenter(request, doc_id):
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
        return HttpResponseRedirect(reverse("app:enter_draft"))

def mydocumententer(request):
    layer = LogbookLayer.objects.filter(doc_type=1).values('alias_name')
    bdldraft = Logbookheader.objects.filter(emp_no=request.user, status='Sending', doc_type=2)

    context = {
        'bdldraft':bdldraft,
        'layer':layer,
    }
    return render(request, 'logbook/entertainment/mydocument.html', context)


def deleteenter(request, doc_id):
    id = doc_id 
    try:
        Entertainment.objects.filter(doc_id=id).delete()
        Logbookbudget.objects.filter(doc_id=id).delete()
        Logbookheader.objects.filter(doc_id=id).delete()
        messages.success(request, "Successfully To Delete   " + str(id))
        return HttpResponseRedirect(reverse("app:bdl_draft"))
    except:
        messages.error(request, "Failed To Delete   " + str(id))
        return HttpResponseRedirect(reverse("app:enter_draft"))


def editenter(request, doc_id):
    listbdl = Entertainment.objects.filter(doc_id=doc_id)
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
    return render(request,'logbook/entertainment/edit.html', context)


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