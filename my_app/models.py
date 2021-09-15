from io import open_code
from typing import Collection
from django.contrib import admin
from django.core.checks import messages
from django.db import models
from django.db.models.base import Model
from django.db.models.deletion import CASCADE, Collector
from django.db.models.fields import related
from django.db.models.fields.related import ForeignKey

# Create your models here.
class Quote(models.Model):
    quote = models.CharField(max_length=200)

    class Meta:
        verbose_name_plural = "Quotes"

    def _str_(self):
        return self.quote

class volunteer(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField("Owner's name",max_length=225)
    password = models.CharField("Password",max_length=100)
    phone = models.CharField("Your Phone Number",max_length=100)
    email = models.EmailField("Your Email")
    address = models.CharField("Your Address",max_length=200)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class home(models.Model):
    id = models.AutoField(primary_key=True)
    owner_name = models.CharField("Owner's name",max_length=225)
    password = models.CharField("Password",max_length=100)
    phone = models.CharField("Your Phone Number",max_length=100)
    email = models.EmailField("Your Email")
    city = models.CharField("Your City",max_length=200)
    state = models.CharField("Your State",max_length=200)
    address = models.CharField("Your Address",max_length=200)
    volunteer = models.ForeignKey(volunteer,on_delete=CASCADE,default=1)
    garbage_collected = models.IntegerField(default=0)
    created_on = models.DateTimeField(auto_now_add=True)
 

    def __str__(self):
        return self.owner_name
        
class shopkeeper(models.Model):
    id = models.AutoField(primary_key=True)
    shopkeepername = models.CharField("Owner's name",max_length=225)
    shop_name = models.CharField("Your Shop name",max_length=255)
    password = models.CharField("Password",max_length=100)
    phone = models.CharField("Your Phone Number",max_length=100)
    email = models.EmailField("Your Email")
    city = models.CharField("Your City",max_length=200)
    state = models.CharField("Your State",max_length=200)
    address = models.CharField("Your Address",max_length=200)
    collector = models.ForeignKey(volunteer,on_delete=CASCADE,related_name="shopkeeper_collector",default=1)
    volunteers = models.ManyToManyField(volunteer, blank=True, related_name="shopkeeper_volunteers")
    garbage_collected = models.IntegerField(default=0)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.shop_name

class garbagecollecter(models.Model):
    id = models.AutoField(primary_key=True)
    garbagecollectorname = models.CharField("Owner's name",max_length=225)
    garbagecollector_company_name = models.CharField("Your Shop name",max_length=255)
    password = models.CharField("Password",max_length=100)
    phone = models.CharField("Your Phone Number",max_length=100)
    email = models.EmailField("Your Email")
    city = models.CharField("Your City",max_length=200)
    state = models.CharField("Your State",max_length=200)
    address = models.CharField("Your Address",max_length=200)
    picker = models.ForeignKey(volunteer,on_delete=CASCADE,related_name="garbagecollector_collector",default=1)
    volunteers = models.ManyToManyField(volunteer, blank=True, related_name="garabgecollector_volunteers")
    garbage_collected = models.IntegerField(default=0)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.garbagecollector_company_name


class company(models.Model):
    category = ( ('F',"Farms or Nurserys"),
                 ('C',"Company"),
                 ('O',"Others"))
    id = models.AutoField(primary_key=True)
    company_owner = models.CharField("Owner's name",max_length=225)
    company_name = models.CharField("Your Shop name",max_length=255)
    category = models.CharField(choices=category,default=1,max_length=225)
    password = models.CharField("Password",max_length=100)
    phone = models.CharField("Your Phone Number",max_length=100)
    email = models.EmailField("Your Email")
    city = models.CharField("Your City",max_length=200)
    state = models.CharField("Your State",max_length=200)
    address = models.CharField("Your Address",max_length=200)
    volunteers = models.ManyToManyField(volunteer, blank=True, related_name="company_volunteers")
    created_on = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.company_name


class contact(models.Model):
    name = models.CharField("Your Name",max_length=224)
    email = models.EmailField("Your Email")
    message = models.TextField("Your Message or Query")

    def __str__(self):
        return self.name
        
class vacancy(models.Model):
    category = ( ('Shopkeeper',"Shopkeeper"),
                 ('GarabgeCollector',"GarbageCollector"),
                 ('Company',"Company"))
    id = models.AutoField(primary_key=True)
    posted_by = models.CharField("Your Name",max_length=224)
    job_title = models.CharField("Job Title",max_length=224)
    job_description = models.TextField("Job Description")
    category = models.CharField(choices=category,max_length=200,default="Shopkeeper")
    
    def __str__(self):
        return self.job_title

class shopvol(models.Model):
    name = models.ForeignKey(volunteer,on_delete=CASCADE)
    list = models.ManyToManyField(home)

class garvol(models.Model):
    name = models.ForeignKey(volunteer,on_delete=CASCADE)
    list = models.ManyToManyField(shopkeeper)

class comvol(models.Model):
    name = models.ForeignKey(volunteer,on_delete=CASCADE)
    list = models.ManyToManyField(garbagecollecter)

class Requests(models.Model):
    id = models.AutoField(primary_key=True)
    req_by = models.ForeignKey(home,on_delete=models.CASCADE)
    req_to = models.ForeignKey(shopkeeper,on_delete=models.CASCADE)
    req_status=models.IntegerField(default=0)
    home_owner_name = models.CharField(max_length=50)
    objects=models.Manager()
    
    def __str__(self):
        return self.home_owner_name

class Requests_S(models.Model):
    id = models.AutoField(primary_key=True)
    req_by = models.ForeignKey(shopkeeper,on_delete=models.CASCADE)
    req_to = models.ForeignKey(garbagecollecter,on_delete=models.CASCADE)
    req_status=models.IntegerField(default=0)
    shop_owner_name = models.CharField(max_length=50)
    objects=models.Manager()
    
    def __str__(self):
        return self.shop_owner_name


class Requests_G(models.Model):
    id = models.AutoField(primary_key=True)
    req_by = models.ForeignKey(garbagecollecter,on_delete=models.CASCADE)
    req_to = models.ForeignKey(company,on_delete=models.CASCADE)
    req_status=models.IntegerField(default=0)
    gar_owner_name = models.CharField(max_length=50)
    objects=models.Manager()
    
    def __str__(self):
        return self.gar_owner_name


class apply(models.Model):
    id = models.AutoField(primary_key=True)
    vol = models.ForeignKey(volunteer,on_delete=CASCADE,default=1)
    posted_by = models.CharField(default="Posted By",max_length=224)
    job_title = models.CharField(default="Job Title",max_length=224)
    job_description = models.TextField(default="Job Description")
    upload = models.FileField(null=True)
    uploaded_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.job_title






        

