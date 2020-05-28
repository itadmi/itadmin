from django.contrib import admin
from switch import models
from django.utils.safestring import mark_safe

# Register your models here.



class SwitchAdmin(admin.ModelAdmin):
    list_display        = ('name','position','ip','type','getData')
    readonly_fields     =('sysDecr','desc')
    list_display_links  =('type','name')
    search_fields   = ('ip','name','position__name')
    fieldsets = [('base',{'fields':['name','ip','position']}),
                 ('snmp get data and write db args',{'fields':['community','version','type','getData','getMacControl']}),
                 ('switch model',{'fields':['sysDecr','desc']})
            ]


    def has_delete_permission(self,request,obj=None):
        return False

class IpMacAdmin(admin.ModelAdmin):
    list_display = ('ip','mac','create','update')
    search_fields= ('ip','mac')
    readonly_fields = ('ip','mac','switch','ipStatus')
    list_display_links = None

    def has_delete_permission(self,request,obj=None):
        return False

    def has_add_permission(self, request):
        return False


class PositionAdmin(admin.ModelAdmin):
    list_display = ('company','floor','name','desc')



class PortAdmin(admin.ModelAdmin):
    list_display= ( 'switch','name','access','index','desc')
    search_fields = ('switch__ip',)
    list_display_links = ('index',)
    list_editable = ('access',)
    readonly_fields= ('switch','name','index')
    fieldsets = [(None,{'fields':['switch','name','access','desc']}),
                ]
    def has_delete_permission(self,request,obj=None):
        return False

    def has_add_permission(self, request):
        return False


class MacAdmin(admin.ModelAdmin):
    list_display= ('get_switch_name','port','mac','computer')
    search_fields = ('mac','port__switch__name')
    list_display_links = None


    def has_delete_permission(self,request,obj=None):
        return False

    def computer(self,obj):
        try:
            computerObj = models.Dhcplease.objects.all().get(clientid=obj.mac)
            return computerObj.hostname
        except:
            return ''
    computer.short_descrition = 'ComputerName'

class UserLoginAdmin(admin.ModelAdmin):
    list_display = ('username','displayname','computerid','remote','logintime','telephone')
    search_fields = ('username','displayname','computerid')
    list_display_links = None
    list_editable = ()
    ordering = ('-logintime',)
    def has_delete_permission(self,request,obj=None):
        return False

    def has_add_permission(self, request):
        return False
    
    def remote(self,obj):
        
        try:
            html= '<a href="RDPDWRCC:{}">{}</a>'.format(obj.computerid,obj.computerid)
            return mark_safe(html)
        except:
            return None


class DhcpleaseAdmin(admin.ModelAdmin):
    list_display = ('hostname','clientid','dhcpid','scopeid','position','switchName','portName')
    search_fields = ('clientid','hostname')
    list_display_links = None

    def has_delete_permission(self,request,obj=None):
        return False

    def macObj(self,obj):
        try:
            mac = models.Mac.objects.all().get(mac=obj.clientid)
            return mac
        except:
            return None

    def portName(self,obj):
        mac = self.macObj(obj)
        if mac:
            return mac.port.name
        else:
            return ''
    portName.short_description = 'Port Name'

    def switchName(self,obj):
        mac = self.macObj(obj)
        if mac:
            return mac.port.switch.name
        else:
            return ''
    
    def position(self,obj):
        mac = self.macObj(obj)
        if mac:
            return mac.port.switch.position.name


admin.site.register(models.Mac,MacAdmin)
#admin.site.register(models.Mac,MacIndexAdmin)
admin.site.register(models.Switch,SwitchAdmin)
admin.site.register(models.IpMac,IpMacAdmin)
admin.site.register(models.Position,PositionAdmin)
admin.site.register(models.Port,PortAdmin)
admin.site.register(models.Dhcplease,DhcpleaseAdmin)
admin.site.register(models.UserLogin,UserLoginAdmin)
