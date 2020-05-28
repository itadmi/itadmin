# _*_ coding: utf-8 _*_

from django.db import models
from switch import define


# Create your models here.
class Position(models.Model):
    id     =  models.AutoField(primary_key=True)
    company=  models.CharField(max_length=260)
    floor  =  models.CharField(max_length=260)
    name  =   models.CharField(max_length=100,unique=True)
    desc = models.CharField(max_length=260,blank=True,default='')
                    
    def __str__(self):  
        return u'%s' % self.name



class Switch(models.Model):
    id        =  models.AutoField(primary_key=True)
    name  = models.CharField(max_length=30,unique=True,verbose_name=u'Switch ID')
    position  = models.ForeignKey(to=Position,on_delete=Position)
    #ip        = models.CharField(max_length=30,unique=True)
    ip         = models.GenericIPAddressField(protocol="ipv4",verbose_name='IP')
    community = models.CharField(max_length=30,default='public')
    version   = models.IntegerField(choices = define.snmpVersion,default=2)
    type      = models.IntegerField(choices = define.swType, default=0)  ##from conf.cf
    getData  = models.IntegerField(default=0,help_text='1:enable 2:initPort 4:getMac 8:getIpMac 16:getVersion 32:makeDesc, default Value 0') 
    getMacControl= models.IntegerField(default=0,help_text='1:standsrtGetmac 2:portAccessCheck 0:default Value ')
    sysDecr = models.TextField(max_length=230,blank=True,default='')
    desc   =  models.TextField(max_length=360,blank=True,default='')
    date  =  models.DateTimeField(auto_now=True)



    class Meta:
        verbose_name_plural = 'SwitchS'

    def __str__(self):
        return '%s' % self.name

    name.short_description = u'Switch name'

class IfDescr(models.Model):
    id     =  models.AutoField(primary_key=True)
    switch =  models.ForeignKey(to=Switch,on_delete=Switch)
    index  =  models.IntegerField()
    descr   =  models.CharField(max_length=50,default='') ##ether1/0/11
    access  =  models.IntegerField(choices = define.ACCESS, default=0)
    date  =  models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural ='port detail'

    def __str__(self):
        return '%s' % self.descr

class Port(models.Model):
    id     =  models.AutoField(primary_key=True)
    switch =  models.ForeignKey(to=Switch,on_delete=Switch,related_name='ports')
    index  =  models.IntegerField()
    name   =  models.CharField(max_length=50,default='') ##ether1/0/11
    access  =  models.IntegerField(choices = define.ACCESS, default=0)
    desc    =  models.CharField(max_length=50,blank=True,default='') ## notice etc access switchName
    date  =  models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural ='port detail'

    def __str__(self):
        return '%s' % self.name

class Mac(models.Model):
    id     =  models.AutoField(primary_key=True)
    port   =  models.ForeignKey(to=Port,on_delete=Port,related_name='macs')
    mac    =  models.CharField(max_length=30,unique=True)
    date   =  models.DateTimeField(auto_now=True)

    def get_switch_name(self):
        return self.port.switch

    def get_computer(self):
        try:
            return Computer.objects.all().get(clientid=self.mac)
        except:
            return ''

class MacIndex(models.Model):
    id     =  models.AutoField(primary_key=True)
    port   =  models.ForeignKey(to=IfDescr,on_delete=IfDescr)
    mac    =  models.CharField(max_length=30,unique=True)
    date   =  models.DateTimeField(auto_now=True) 

class IpMac(models.Model):
    id       =  models.AutoField(primary_key=True)
    switch    =  models.ForeignKey(to=Switch,on_delete=Switch)  ###core switch get IP mac
    ip       =  models.CharField(max_length=30,unique=True)
    mac      =  models.CharField(max_length=30)
    create   =  models.DateTimeField(auto_now_add=True)
    update   =  models.DateTimeField(auto_now=True)
    ipStatus =  models.IntegerField(choices = define.ipStatus, default=1)  ## default On Line ,0 OffLine

    class Meta:
        verbose_name_plural = 'IP Map Address'



class Dhcplease(models.Model):
    id       =  models.AutoField(primary_key=True)
    dhcpid   =  models.CharField(max_length=30)
    clientid =  models.CharField(max_length=50,default='')
    hostname =  models.CharField(max_length=50,default='')
    scopeid  =  models.CharField(max_length=50,default='')

class UserLogin(models.Model):
    id       =  models.AutoField(primary_key=True)
    username = models.CharField(max_length=50,default='')
    displayname= models.CharField(max_length=50,default='')
    computerid = models.CharField(max_length=50,default='')
    telephone  = models.CharField(max_length=50,default='')
    logintime  = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'login'
