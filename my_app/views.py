from django import http
from django.http.request import HttpRequest
from django.http.response import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib.auth import login, logout, authenticate
from .models import *
from django.contrib import messages
from django.db.models import Q
from django.conf import settings
import os

# Create your views here.
       
def signup(request):
    return render(request,"signup.html")

def login(request):
    return render(request, 'login.html')

def contact_form(request):
    if request.method == 'POST':
        name=request.POST.get("txtName")
        email=request.POST.get("txtEmail")
        message=request.POST.get("txtMsg")
        msg=contact.objects.create(name=name,email=email,message=message)
        msg.save()
        return redirect(index)

def index(request):
    random_quote = Quote.objects.order_by("?").first()
    context = {'random_quote' : random_quote}
    return render(request, 'index.html', context)

#<============Home===================>

def home_login(request):
    return render(request,"home/login_home.html")

def home_edit(request, id):
    details = home.objects.get(id=id)
    context = {'details': details}
    return render(request, 'home/home_edit.html', context)

def home_update(request, id):  
    details = home.objects.get(id=id)
    if request.method == 'POST':
        details.owner_name = request.POST['username']
        details.phone = request.POST['phone']
        details.email = request.POST['email']
        details.address = request.POST['address']
        details.city = request.POST['city']
        details.state = request.POST['state']
        details.password = request.POST['password1']
        details.save()
        return redirect('profile_home',details.id)

def home_page(request):
    if request.method == 'POST':
        if home.objects.filter(email=request.POST['email'], password=request.POST['password']).exists():
            member = home.objects.get(email=request.POST['email'], password=request.POST['password'])
            return render(request, 'home/home_page.html', {'member': member})
        else:
            messages.error(request,"Invalid Credentials")
            return redirect(home_login)
    else:
        return render(request,'home/login_home.html')

def home_profile(request,id):
    member = home.objects.get(id=id)
    return render(request,'home/home_page.html',{'member':member})

def do_home_signup(request):
    if request.method == "POST":
        username=request.POST.get("username")
        password1=request.POST.get("password1")
        password2=request.POST.get("password2")
        phone=request.POST.get("phone")
        email=request.POST.get("email")
        city=request.POST.get("city")
        state=request.POST.get("state")
        address=request.POST.get("address")
        if password1 == password2:
            if home.objects.filter(email=request.POST['email']).exists():
                messages.error(request,"Email already exists !")
            else:
                user=home.objects.create(owner_name=username,password=password1,phone=phone,email=email,city=city,state=state,address=address)
                user.save()
                messages.success(request,"Successfully Created Your Account.")
                return redirect(home_login)
        else:
            messages.error(request,"Password doesn't match !")
        return render(request,"home/sign_home_page.html")   
    else:
        return render(request, 'home/sign_home_page.html', {})

def search_shopkeeper(request,id):
    data = home.objects.get(id=id)
    return render(request,"home/home_search.html",{'data':data})
        
def shopkeepersearch(request,id):    
    data = home.objects.get(id=id)
    count = 0
    if request.method == "POST":
        state = request.POST.get('state')
        city = request.POST.get('city')
        lookup = (Q(state__icontains=state) and Q(city__icontains=city))
        shop = shopkeeper.objects.filter(lookup)
        return render(request, 'home/home_search.html', {'shop':shop,'data':data})
    else:
        return render(request, 'home/home_search.html', {'data':data,'count' : count})

def Request(request, home_id, shop_id):
    h_obj = home.objects.get(id=home_id)
    s_obj = shopkeeper.objects.get(id=shop_id)
    req = Requests(req_by=h_obj,req_to=s_obj,home_owner_name=h_obj.owner_name)
    req.save()
    return HttpResponseRedirect(reverse('ShopKeepers', args = (home_id,)))

def ShopKeepers(request,home_id):
    r_objects = Requests.objects.filter(req_by=home_id)
    count = 0
    for robj in r_objects:
        if(robj.req_status == 0):
            count = 1
            break;
    return render(request, 'home/home_msg.html', { 'home_id' : home_id, 'r_objects' : r_objects, 'count' : count,})


        
#<====================Shopkeeper================================>

def shopkeeper_login(request):
    return render(request,"shopkeeper/login_shopkeeper.html")

def shop_edit(request, id):
    details = shopkeeper.objects.get(id=id)
    context = {'details': details}
    return render(request, 'shopkeeper/shop_edit.html', context)

def shop_update(request, id):  
    details = shopkeeper.objects.get(id=id)
    if request.method == 'POST':
        details.shopkeepername = request.POST['username']
        details.shop_name = request.POST['shopname']
        details.phone = request.POST['phone']
        details.email = request.POST['email']
        details.address = request.POST['address']
        details.city = request.POST['city']
        details.state = request.POST['state']
        details.password = request.POST['password1']
        details.save()
        return redirect('profile_shopkeeper',details.id)

def shopkeeper_home(request):
    if request.method == 'POST':
        if shopkeeper.objects.filter(email=request.POST['email'], password=request.POST['password']).exists():
            member = shopkeeper.objects.get(email=request.POST['email'], password=request.POST['password'])
            return render(request,'shopkeeper/shopkeeper_page.html',{'member':member})
        else:
            messages.error(request,"Invalid Credentials")
            return redirect(shopkeeper_login)
    else:
        return render(request,'shopkeeper/login_shopkeeper.html')

def shopkeeper_profile(request,id):
    member = shopkeeper.objects.get(id=id)
    return render(request,'shopkeeper/shopkeeper_page.html',{'member':member})
    
def do_shopkeeper_signup(request):
    if request.method == "POST":
        username=request.POST.get("username")
        shopname = request.POST.get("shopname")
        password1=request.POST.get("password1")
        password2=request.POST.get("password2")
        phone=request.POST.get("phone")
        email=request.POST.get("email")
        city=request.POST.get("city")
        state=request.POST.get("state")
        address=request.POST.get("address")
        if password1 == password2:
            try:
                if shopkeeper.objects.filter(email=request.POST['email']).exists():
                    messages.error(request,"Email already exists !")
                else:
                    user=shopkeeper.objects.create(shopkeepername=username,shop_name=shopname,password=password1,phone=phone,email=email,city=city,state=state,address=address)
                    user.save()
                    messages.success(request,"Successfully Created Your Account")
                    return redirect(shopkeeper_login)
            except:
                messages.error(request,"Failed to Create Your Account !")
        else:
            messages.error(request,"Password doesn't match !")
        return render(request,"shopkeeper/sign_shopkeeper_page.html")   
    else:
        return render(request, 'shopkeeper/sign_shopkeeper_page.html', {})

def search_garbagecollector(request,id):
    data = shopkeeper.objects.get(id=id)
    return render(request,"shopkeeper/shopkeeper_search.html",{'data':data})
        
def garbagecollectorsearch(request,id):
    data = shopkeeper.objects.get(id=id)
    if request.method == "POST":
        state = request.POST.get('state')
        city = request.POST.get('city')
        lookup = (Q(state__icontains=state) and Q(city__icontains=city))
        shop = garbagecollecter.objects.filter(lookup)
        return render(request, 'shopkeeper/shopkeeper_search.html', {'shop':shop,'data':data})
    else:
        return render(request, 'shopkeeper/shopkeeper_search.html', {'data':data})


def vacancy_shop(request,id):
    i = shopkeeper.objects.get(id=id)
    if request.method == "POST":
        posted = vacancy.objects.filter(posted_by = i.shop_name )
        posted_by = request.POST.get('posted_by')
        title = request.POST.get('title')
        description = request.POST.get('description')
        offer = vacancy.objects.create(posted_by=posted_by,job_title=title,job_description=description)
        offer.save()
        messages.success(request,"Successfully Updated")
        return render(request,"shopkeeper/shop_vacany.html",{'i':i,'posted' : posted})
    else:
        posted = vacancy.objects.filter(posted_by = i.shop_name )
        return render(request, 'shopkeeper/shop_vacany.html', {'i':i,'posted' : posted})

def Requests_view(request, id):
    s_obj = shopkeeper.objects.get(id=id)
    req_objects = Requests.objects.all().filter(req_to=id)
    return render(request, 'shopkeeper/shop_msg.html', {'req_objects' : req_objects, 's_obj' : s_obj})

def accept_req(request,id):
    r_obj = Requests.objects.get(id=id)
    r_obj.req_status = 1
    r_obj.save()
    return render(request,"shopkeeper/shop_req.html",{'r_obj': r_obj})

def decline_req(request, id):
    r_obj = Requests.objects.get(id=id)
    r_obj.req_status = 2
    r_obj.save()
    messages.error(request,"Request is Declined")  
    return render(request,"shopkeeper/shop_req.html",{'r_obj': r_obj})
 
def Request_shop(request, shop_id, gar_id):
    h_obj = shopkeeper.objects.get(id=shop_id)
    s_obj = garbagecollecter.objects.get(id=gar_id)
    req = Requests_S(req_by=h_obj,req_to=s_obj,shop_owner_name=h_obj.shop_name)
    req.save()
    return HttpResponseRedirect(reverse('GarbageCollectors', args = (shop_id,)))

def GarbageCollectors(request,shop_id):
    r_objects = Requests_S.objects.filter(req_by=shop_id)
    count = 0
    for robj in r_objects:
        if(robj.req_status == 0):
            count = 1
            break;
    return render(request, 'shopkeeper/shop_not.html', { 'shop_id' : shop_id, 'r_objects' : r_objects, 'count' : count,})

def application_shop(request,id):
    shop = shopkeeper.objects.get(id=id)
    applications = apply.objects.filter(posted_by=shop.shop_name)
    return render(request,"shopkeeper/shop_app.html",{'shop':shop,'applications':applications})

def add_shop(request,vol_id,shop):
    vol = volunteer.objects.get(id=vol_id)
    shop = shopkeeper.objects.get(id=shop)
    if request.method == "POST":
       shop.volunteers.add(vol)
       shop.save()
       messages.success(request,"volunteer is approved")
       return render(request,"shopkeeper/shop_app.html",{'shop':shop})

def decline_shop(request,vol_id,shop):
    vol = volunteer.objects.get(id=vol_id)
    shop = shopkeeper.objects.get(id=shop)
    if request.method == "POST":
        if apply.objects.filter(vol=vol,posted_by=shop.shop_name).exists():
            post = apply.objects.get(vol=vol,posted_by=shop.shop_name)
            post.delete() 
            messages.error(request,"volunteer is Declined")
        return redirect('profile_shopkeeper',shop.id)


def Houses_list(request,id):
    shop = shopkeeper.objects.get(id=id)
    home = Requests.objects.filter(req_to=shop,req_status=1)
    return render(request,"shopkeeper/house_list.html",{'shop':shop,'home':home})

def change_vol(request,id):
    shop = shopkeeper.objects.get(id=id)
    home = Requests.objects.filter(req_to=shop,req_status=1)
    return render(request,"shopkeeper/house_list.html",{'shop':shop,'home':home})

def assign_home(request,shop,h):
    shop = shopkeeper.objects.get(id=shop)
    h = home.objects.get(id=h)
    if request.method == "POST":
        vol_assign = request.POST.get("vol_assign")
        vol = volunteer.objects.get(id=vol_assign)
        h.volunteer = vol
        h.save()
        messages.success(request,"volunteer is assigned")
        return render(request,"shopkeeper/house_list.html",{'shop':shop,'h':h})

#<====================GarabgeCollector================================>

def garbagecollector_login(request):
    return render(request,"garbagecollector/login_garbagecollector.html")

def gar_edit(request, id):
    details = garbagecollecter.objects.get(id=id)
    context = {'details': details}
    return render(request, 'garbagecollector/gar_edit.html', context)

def gar_update(request, id):  
    details = garbagecollecter.objects.get(id=id)
    if request.method == 'POST':
        details.garbagecollectorname = request.POST['username']
        details.garbagecollector_company_name = request.POST['shopname']
        details.phone = request.POST['phone']
        details.email = request.POST['email']
        details.address = request.POST['address']
        details.city = request.POST['city']
        details.state = request.POST['state']
        details.password = request.POST['password1']
        details.save()
        return redirect('profile_garbagecollector',details.id)

def garbagecollector_home(request):
    if request.method == 'POST':
        if garbagecollecter.objects.filter(email=request.POST['email'], password=request.POST['password']).exists():
            member = garbagecollecter.objects.get(email=request.POST['email'], password=request.POST['password'])
            return render(request, 'garbagecollector/garbagecollector_page.html', {'member': member})
        else:
            messages.error(request,"Invalid Credentials")
            return redirect(garbagecollector_login)
    else:
        return render(request,'garbagecollector/login_garbagecollector.html')

def garbagecollector_profile(request,id):
    member = garbagecollecter.objects.get(id=id)
    return render(request,'garbagecollector/garbagecollector_page.html',{'member':member})

def do_garbagecollecter_signup(request):
    if request.method == "POST":
        username=request.POST.get("username")
        garbagecollector_company_name = request.POST.get("companyname")
        password1=request.POST.get("password1")
        password2=request.POST.get("password2")
        phone=request.POST.get("phone")
        email=request.POST.get("email")
        city=request.POST.get("city")
        state=request.POST.get("state")
        address=request.POST.get("address")
        if password1 == password2:
            try:
                if garbagecollecter.objects.filter(email=request.POST['email']).exists():
                    messages.error(request,"Email already exists !")
                else:
                    user=garbagecollecter.objects.create(garbagecollectorname=username,garbagecollector_company_name=garbagecollector_company_name,password=password1,phone=phone,email=email,city=city,state=state,address=address)
                    user.save()
                    messages.success(request,"Successfully Created Account. ")
                    return redirect(garbagecollector_login)
            except:
                messages.error(request,"Failed to Create Your Account")
        else:
            messages.error(request,"Password doesn't match !")
        return render(request,"garbagecollector/sign_garbagecollector_page.html") 
    else:
        return render(request, 'garbagecollector/sign_garbagecollector_page.html', {})

def search_company(request,id):
    data = garbagecollecter.objects.get(id=id)
    return render(request,"garbagecollector/company_search.html",{'data':data})
        
def companysearch(request,id):
    data = garbagecollecter.objects.get(id=id)
    if request.method == "POST":
        state = request.POST.get('state')
        city = request.POST.get('city')
        lookup = (Q(state__icontains=state) and Q(city__icontains=city))
        shop = company.objects.filter(lookup)
        return render(request, 'garbagecollector/company_search.html', {'shop':shop,'data':data}) 
    else:
        return render(request, 'garbagecollector/company_search.html', {'data':data})    

def vacancy_garbagecollector(request,id):
    i = garbagecollecter.objects.get(id=id)
    if request.method == "POST":
        posted = vacancy.objects.filter(posted_by = i.garbagecollector_company_name )
        posted_by = request.POST.get('posted_by')
        title = request.POST.get('title')
        description = request.POST.get('description')
        offer = vacancy.objects.create(posted_by=posted_by,job_title=title,job_description=description)
        offer.save()
        messages.success(request,"Successfully Updated")
        return render(request,"garbagecollector/garbagecollector_vacany.html",{'i':i,'posted' : posted})
    else:
        posted = vacancy.objects.filter(posted_by = i.garbagecollector_company_name )
        return render(request, 'garbagecollector/garbagecollector_vacany.html', {'i':i,'posted' : posted})

def Requests_view_shop(request, id):
    s_obj = garbagecollecter.objects.get(id=id)
    req_objects = Requests_S.objects.all().filter(req_to=id)
    return render(request, 'garbagecollector/gar_msg.html', {'req_objects' : req_objects, 's_obj' : s_obj})

def accept_req_shop(request,id):
    r_obj = Requests_S.objects.get(id=id)
    r_obj.req_status = 1
    r_obj.save()
    return render(request,"garbagecollector/gar_req.html",{'r_obj': r_obj})

def decline_req_shop(request,id):
    r_obj = Requests_S.objects.get(id=id)
    r_obj.req_status = 2
    r_obj.save()
    return render(request,"garbagecollector/gar_req.html",{'r_obj': r_obj})
 
def Request_gar(request, gar_id, com_id):
    h_obj = garbagecollecter.objects.get(id=gar_id)
    s_obj = company.objects.get(id=com_id)
    req = Requests_G(req_by=h_obj,req_to=s_obj, gar_owner_name=h_obj.garbagecollector_company_name)
    req.save()
    return HttpResponseRedirect(reverse('Company', args = (gar_id,)))

def Company(request,gar_id):
    r_objects = Requests_G.objects.filter(req_by=gar_id)
    count = 0
    for robj in r_objects:
        if(robj.req_status == 0):
            count = 1
            break;
    return render(request, 'garbagecollector/gar_not.html', { 'gar_id' : gar_id, 'r_objects' : r_objects, 'count' : count,})

def application_gar(request,id):
    shop = garbagecollecter.objects.get(id=id)
    applications = apply.objects.filter(posted_by=shop.garbagecollector_company_name)
    return render(request,"garbagecollector/gar_app.html",{'shop':shop,'applications':applications})

def add_gar(request,vol_id,shop):
    vol = volunteer.objects.get(id=vol_id)
    shop = garbagecollecter.objects.get(id=shop)
    if request.method == "POST":
       shop.volunteers.add(vol)
       shop.save()
       messages.success(request,"volunteer is approved")
       return render(request,"garbagecollector/gar_app.html",{'shop':shop})

def decline_gar(request,vol_id,shop):
    vol = volunteer.objects.get(id=vol_id)
    shop = garbagecollecter.objects.get(id=shop)
    if request.method == "POST":
        if apply.objects.filter(vol=vol,posted_by=shop.garbagecollector_company_name).exists():
            post = apply.objects.get(vol=vol,posted_by=shop.garbagecollector_company_name)
            post.delete() 
            messages.error(request,"volunteer is Declined")
        return redirect('profile_garbagecollector',shop.id)


def Shops_list(request,id):
    shop = garbagecollecter.objects.get(id=id)
    home = Requests_S.objects.filter(req_to=shop,req_status=1)
    return render(request,"garbagecollector/shops_list.html",{'shop':shop,'home':home})

def change_vol_gar(request,id):
    shop = garbagecollecter.objects.get(id=id)
    home = Requests_S.objects.filter(req_to=gar,req_status=1)
    return render(request,"garbagecollector/shops_list.html",{'shop':shop,'home':home})

def assign_shop(request,shop,h):
    shop = garbagecollecter.objects.get(id=shop)
    h = shopkeeper.objects.get(id=h)
    if request.method == "POST":
        vol_assign = request.POST.get("vol_assign")
        vol = volunteer.objects.get(id=vol_assign)
        h.collector = vol
        h.save()
        messages.success(request,"volunteer is assigned")
        return render(request,"garbagecollector/shops_list.html",{'shop':shop,'h':h})

#<====================Company=============================>

def company_login(request):
    return render(request,"company/login_company.html")

def com_edit(request, id):
    details = company.objects.get(id=id)
    context = {'details': details}
    return render(request, 'company/com_edit.html', context)

def com_update(request, id):  
    details = company.objects.get(id=id)
    if request.method == 'POST':
        details.gcompany_owner = request.POST['username']
        details.company_name = request.POST['shopname']
        details.phone = request.POST['phone']
        details.email = request.POST['email']
        details.address = request.POST['address']
        details.city = request.POST['city']
        details.state = request.POST['state']
        details.password = request.POST['password1']
        details.save()
        return redirect('profile_company',details.id)

def company_home(request):
    if request.method == 'POST':
        if company.objects.filter(email=request.POST['email'], password=request.POST['password']).exists():
            member = company.objects.get(email=request.POST['email'], password=request.POST['password'])
            return render(request, 'company/company_page.html', {'member': member})
        else:
            messages.error(request,"Invalid Credentials")
            return redirect(company_login)
    else:
        return render(request,'company/login_company.html')
    
def company_profile(request,id):
    member = company.objects.get(id=id)
    return render(request,'company/company_page.html',{'member':member})

def do_company_signup(request):
    if request.method == "POST":
        username=request.POST.get("username")
        company_name = request.POST.get("companyname")
        password1=request.POST.get("password1")
        password2=request.POST.get("password2")
        phone=request.POST.get("phone")
        email=request.POST.get("email")
        city=request.POST.get("city")
        state=request.POST.get("state")
        address=request.POST.get("address")
        if password1 == password2:
            try:
                if company.objects.filter(email=request.POST['email']).exists():
                    messages.error(request,"Email already exists !")
                else:
                    user=company.objects.create(company_owner=username,company_name=company_name,password=password1,phone=phone,email=email,city=city,state=state,address=address)
                    user.save()
                    messages.success(request,"Successfully Created Account")
                    return redirect(company_login)
            except:
                messages.error(request,"Failed to Create Account")
        else:
            messages.error(request,"Password doesn't match !")
        return render(request,"company/sign_company_page.html")
    else:
        return render(request, 'company/sign_company_page.html', {})

def vacancy_company(request,id):
    i = company.objects.get(id=id)
    if request.method == "POST":
        posted = vacancy.objects.filter(posted_by = i.company_name )
        posted_by = request.POST.get('posted_by')
        title = request.POST.get('title')
        description = request.POST.get('description')
        offer = vacancy.objects.create(posted_by=posted_by,job_title=title,job_description=description)
        offer.save()
        messages.success(request,"Successfully Updated")
        return render(request,"company/company_vacany.html",{'i':i,'posted' : posted})
    else:
        posted = vacancy.objects.filter(posted_by = i.company_name )
        return render(request, 'company/company_vacany.html', {'i':i,'posted' : posted})

def Requests_view_gar(request, id):
    s_obj = company.objects.get(id=id)
    req_objects = Requests_G.objects.all().filter(req_to=id)
    return render(request, 'company/com_msg.html', {'req_objects' : req_objects, 's_obj' : s_obj})

def accept_req_gar(request,id):
    r_obj = Requests_G.objects.get(id=id)
    r_obj.req_status = 1
    r_obj.save()
    return render(request,"company/com_req.html",{'r_obj': r_obj})

def decline_req_gar(request,id):
    r_obj = Requests_G.objects.get(id=id)
    r_obj.req_status = 2
    r_obj.save()
    return render(request,"company/com_req.html",{'r_obj': r_obj})

def application_com(request,id):
    shop = company.objects.get(id=id)
    applications = apply.objects.filter(posted_by=shop.company_name)
    return render(request,"company/com_app.html",{'shop':shop,'applications':applications})

def Gar_list(request,id):
    shop = company.objects.get(id=id)
    home = Requests_G.objects.filter(req_to=shop,req_status=1)
    return render(request,"company/gars_list.html",{'shop':shop,'home':home})

def add_com(request,vol_id,shop):
    vol = volunteer.objects.get(id=vol_id)
    shop = company.objects.get(id=shop)
    if request.method == "POST":
       shop.volunteers.add(vol)
       shop.save()
       messages.success(request,"volunteer is approved")
       return render(request,"company/com_app.html",{'shop':shop})

def decline_com(request,vol_id,shop):
    vol = volunteer.objects.get(id=vol_id)
    shop = company.objects.get(id=shop)
    if request.method == "POST":
        if apply.objects.filter(vol=vol,posted_by=shop.company_name).exists():
            post = apply.objects.get(vol=vol,posted_by=shop.company_name)
            post.delete() 
            messages.error(request,"volunteer is Declined")
        return redirect('profile_company',shop.id)

def change_vol_com(request,id):
    shop = company.objects.get(id=id)
    home = Requests_G.objects.filter(req_to=shop,req_status=1)
    return render(request,"company/gars_list.html",{'shop':shop,'home':home})

def assign_gar(request,shop,h):
    shop = company.objects.get(id=shop)
    h = garbagecollecter.objects.get(id=h)
    if request.method == "POST":
        vol_assign = request.POST.get("vol_assign")
        vol = volunteer.objects.get(id=vol_assign)
        h.collector = vol
        h.save()
        messages.success(request,"volunteer is assigned")
        return render(request,"company/gars_list.html",{'shop':shop,'h':h})

#<====================Volunteer=============================>

def volunteer_login(request):
    return render(request,"volunteer/login_volunteer.html")

def vol_edit(request, id):
    details = volunteer.objects.get(id=id)
    context = {'details': details}
    return render(request, 'volunteer/vol_edit.html', context)

def vol_update(request, id):  
    details = volunteer.objects.get(id=id)
    if request.method == 'POST':
        details.name = request.POST['username']
        details.phone = request.POST['phone']
        details.email = request.POST['email']
        details.address = request.POST['address']
        details.password = request.POST['password1']
        details.save()
        return redirect('profile_volunteer',details.id)

def volunteer_home(request):
    if request.method == 'POST':
        if volunteer.objects.filter(email=request.POST['email'], password=request.POST['password']).exists():
            member = volunteer.objects.get(email=request.POST['email'], password=request.POST['password'])
            return render(request, 'volunteer/volunteer_page.html', {'member': member})
        else:
            messages.error(request,"Invalid Credentials")
            return redirect(volunteer_login)
    else:
        return render(request,'volunteer/login_volunteer.html')

def volunteer_profile(request,id):
    member = volunteer.objects.get(id=id)
    return render(request,'volunteer/volunteer_page.html',{'member':member})

def do_volunteer_signup(request):
    if request.method == "POST":
        username=request.POST.get("username")
        phone=request.POST.get("phone")
        email=request.POST.get("email")
        password1=request.POST.get("password1")
        password2=request.POST.get("password2")
        address=request.POST.get("address")
        if password1 == password2:
            try:
                if volunteer.objects.filter(email=request.POST['email']).exists():
                    messages.error(request,"Email already exists !")
                else:
                    user=volunteer.objects.create(name=username,password=password1,phone=phone,email=email,address=address)
                    user.save()
                    messages.success(request,"Successfully Created Account")
                    return redirect(volunteer_login)
            except:
                messages.error(request,"Failed to Create Account")
        else:
            messages.error(request,"Password doesn't match !")
        return render(request,"volunteer/sign_volunteer_page.html")
    else:
        return render(request, 'volunteer/sign_volunteer_page.html', {})

def jobopp(request,id):
    member = volunteer.objects.get(id=id)
    list = vacancy.objects.all()
    return render(request,"volunteer/volunteer_vacany.html",{'list':list,'member':member})

def home_list(request,id):
    vol = volunteer.objects.get(id=id)
    if home.objects.filter(volunteer=vol).exists():
        i = home.objects.filter(volunteer=vol)
    elif shopkeeper.objects.filter(collector=vol).exists():
        i = shopkeeper.objects.filter(collector=vol)
    else:
        i = garbagecollecter.objects.filter(picker=vol)
    return render(request,"volunteer/homelist.html",{'i':i,'vol':vol})

def home_collect(request,id):
    i = home.objects.get(id=id)
    if request.method == "POST":
        col = request.POST.get("collection")
        num = int(col)
        update = num + i.garbage_collected
        i.garbage_collected = update
        i.save()
        messages.success(request,"Updated")
        return redirect('profile_volunteer',i.volunteer.id)

def shop_collect(request,id):
    i = shopkeeper.objects.get(id=id)
    if request.method == "POST":
        col = request.POST.get("collection")
        num = int(col)
        update = num + i.garbage_collected
        i.garbage_collected = update
        i.save()
        messages.success(request,"Updated")
        return redirect('profile_volunteer',i.collector.id)


def gar_collect(request,id):
    i = garbagecollecter.objects.get(id=id)
    if request.method == "POST":
        col = request.POST.get("collection")
        num = int(col)
        update = num + i.garbage_collected
        i.garbage_collected = update
        i.save()
        messages.success(request,"Updated")
        return redirect('profile_volunteer',i.picker.id)


def logout_user(request):
    if request.method == "POST":
        logout(request)
        return redirect('index')

def delete(request, id):  
    details = vacancy.objects.get(id=id)  
    details.delete() 
    return redirect('/')

def application(request,vol_id,job_id):
    vol = volunteer.objects.get(id=vol_id)
    job = vacancy.objects.get(id=job_id)
    return render(request,"apply.html",{'vol':vol,'job':job})


def upload(request,id):
    vol = volunteer.objects.get(id=id)
    if request.method == 'POST':
        posted_by = request.POST.get("posted_by")
        job_title = request.POST.get("job_title")
        job_description = request.POST.get("job_description")
        upload = request.FILES["upload"]
        filename = apply.objects.create(vol=vol,job_title=job_title,job_description=job_description,upload=upload,posted_by=posted_by)
        filename.save()
        messages.success(request,"Your Application as been sent !")
        return redirect('profile_volunteer',vol.id)
    


