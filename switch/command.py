import time,sys
from switch import oid,models,base,define
from switch.base import decorate

from switch.define import GET_DATA
from switch.log import logger


class Default(metaclass=base.metaclass):
    def __init__(self):
        self.sections = base.Config().sections
         
    @decorate('command','_command')
    def _command(self,*args,**kwargs):
        switchObj = kwargs['switchObj']
        get_data   = switchObj.getData

        get_data_function = switchObj.get_data_function
        func_value = GET_DATA[get_data_function]
        
        if define.GET_DATA['enable'] & switchObj.getData == 0:
            kwargs['message'] = '    switch getData is 0'; logger.error(**kwargs)
            return None

        kwargs['message'] ='switch name:%s getDataValue:%s, define.GET_DATA[%s] = %s ' % \
                            (switchObj.name,get_data,get_data_function,func_value)
        logger.info(**kwargs)

        if func_value != get_data & func_value:
            kwargs['message'] = '%s:%s return None' %(switchObj.name,switchObj.oidName);logger.info(**kwargs)
            return None

        oidClass,oidFunc = base.get_class_func(model=oid,switchObj=switchObj)

        ##call Oid function
        oidObj = oidClass()
        generic =oidFunc(oidObj,switchObj=switchObj)

        return generic
   
    @decorate('command','initPort')
    def initPort(self,*args,**kwargs):
        switchObj = kwargs['switchObj']
        switchObj.func = 'initPort'


        # get dot1dBasePortIfIndex
        #oidName = dot1dBasePortIfIndex
        kwargs['message'] = 'start get dot1dBasePortIfIndex oid value'; logger.info(**kwargs)

        switchObj.oidName = 'dot1dBasePortIfIndex'
        index_generic = self._command(**kwargs)
        if not index_generic:
            kwargs['message'] = '     get dot1dBasePortIfIndex oid value is None'; logger.error(**kwargs)
            return None
        kwargs['message'] = '      get dot1dBasePortIfIndex oid value number: %s' % len(index_generic); logger.info(**kwargs)

        
        kwargs['message'] = 'start get ifName oid value'; logger.info(**kwargs)
        switchObj.oidName = 'ifName'
        name_generic = self._command(**kwargs)
        if not name_generic:
             kwargs['message'] = '     get ifName oid value is None'; logger.error(**kwargs)
             return None

        kwargs['message'] = '      get ifName oid value number: %s' % len(name_generic); logger.info(**kwargs)



        # delete port set and mac set
        portSet = switchObj.ports.all()
        if len(portSet) > 0:
            for port in portSet:
                port.macs.all().delete()
            portSet.delete()
        
        ##create index mac
        for index2,index in index_generic.items():
            try:
                models.Port.objects.create(switch=switchObj,index=index2,name=name_generic[index])
            except:
                print(index,index2)
                print(name_generic)


    
        switchObj.getData = switchObj.getData - define.GET_DATA[switchObj.get_data_function]
        switchObj.save()
        return True
    def _standard_getMac(self,*args,**kwargs):

        switchObj = kwargs['switchObj']
        
        ##get index map port
        portSet = switchObj.ports.all()
        if len(portSet) == 0:
            kwargs['message'] = '      portSet number is 0,please initPort';  logger.error(**kwargs)
            logger.error(**kwargs)
            return None


        portObj_index = {}
        for port in portSet:
            portObj_index[port.index] = port
        

        ## get oid:dot1dTpFdbPort --index_generic[mac1]=index--
        switchObj.oidName = 'dot1dTpFdbPort'
        index_generic = self._command(*args,**kwargs)
        if not index_generic:
            kwargs['message'] = '    get oid:dot1dTpFdbPort return None'; logger.error(**kwargs)
            return None

        index_number = len(index_generic)
        kwargs['message'] = '    get oid:dot1dTpFdbPort generic number: %s' % index_number
        logger.info(**kwargs)

        ## get oid:dot1dTpFdbPort --address_generic[mac]=mac1
        switchObj.oidName = 'dot1dTpFdbAddress'
        address_generic = self._command(*args,**kwargs)
        if not address_generic:
            kwargs['message'] = '    get oid:dot1dTpFdbAddress return None'; logger.error(**kwargs)
            logger.info(**kwargs)
            return None
        else:
            address_number = len(address_generic)        
        kwargs['message'] = '    get oid:dot1dTpFdbAddress generic number: %s' % address_number 
        logger.info(**kwargs)

        
        ##get mac_port[mac] = port
        mac_port = {}        
        for address,address2 in address_generic.items():
            try:
                mac_port[address] = portObj_index[index_generic[address2]]
            except:
                kwargs['message'] = 'mac:%s in dot1dTpFdbAddress but not in dot1dTpFdbPort' % address;logger.info(**kwargs)
     
 

        ## make port_macList[port]= [mac list]
        port_macList = {}
        for mac,port in mac_port.items():
            try:
                port_macList[port].append(mac)
            except:
                port_macList[port] = []
                port_macList[port].append(mac)

        ##make mac[macAddress] = macObj
        macSet = models.Mac.objects.all()
        macDict = {}
        macDictKeys = []
        for macObj in macSet:
            macDictKeys.append(macObj.mac)
            macDict[macObj.mac] = macObj

        if switchObj.getMacControl & define.GET_MAC_CONTROL['port_access_check'] == define.GET_MAC_CONTROL['port_access_check'] :
            for portObj,macList in port_macList.items():
                if portObj.access != 0:  ## 端口接非交换机
                    for mac in macList:
                        if mac in macDictKeys:
                            if macDict[mac].port != portObj:
                                macDict[mac].port = portObj
                                macDict[mac].save()
                        else:
                            models.Mac.objects.create(port=portObj,mac=mac)      
        else:
            ##没有开启端口检测，所有端口Mac都写入DB
            for portObj,macList in port_macList.items():
                if len(macList) < define.MaxMacPortNumber:
                    for mac in macList:
                        if mac in macDictKeys:
                            if macDict[mac].port != portObj:
                                macDict[mac].port = portObj
                                macDict[mac].save()
                        else:
                            models.Mac.objects.create(port=portObj,mac=mac)

        return True
             
    @decorate('command.default','nonStandardGetmac')
    def _non_standard_getMac(self,*args,**kwargs):
        switchObj = kwargs['switchObj']
        
        ##get index map port
        portSet = switchObj.ports.all()
        if len(portSet) == 0:
            kwargs['message'] = '      portSet number is 0,please initPort';  logger.error(**kwargs)
            logger.error(**kwargs)
            return None
        portObj_index = {}
        for port in portSet:
            portObj_index[port.index] = port
        

        ## get oid:dot1dTpFdbPort --index_generic[mac1]=index--
        switchObj.oidName = 'dot1dTpFdbPort'
        index_generic = self._command(*args,**kwargs)
        if not index_generic:
            kwargs['message'] = '    get oid:dot1dTpFdbPort return None'; logger.error(**kwargs)
            return None
        index_number = len(index_generic)
        kwargs['message'] = '    get oid:dot1dTpFdbPort generic number: %s' % index_number
        logger.info(**kwargs)

        
        ##get mac_port[mac] = port
        mac_port = {}        
        for mac,index in index_generic.items():
            try:
                mac_port[mac] = portObj_index[index]
            except:
                pass
     

        ## make port_macList[port]= [mac list]
        port_macList = {}
        for mac,port in mac_port.items():
            try:
                port_macList[port].append(mac)
            except:
                port_macList[port] = []
                port_macList[port].append(mac)

        ##make mac[macAddress] = macObj
        macSet = models.Mac.objects.all()
        macDict = {}
        macDictKeys = []
        for macObj in macSet:
            macDictKeys.append(macObj.mac)
            macDict[macObj.mac] = macObj

        ##getMacControl
        ##standard_getMac = 1
        #port_access_check = 2
        if switchObj.getMacControl & define.GET_MAC_CONTROL['port_access_check'] == define.GET_MAC_CONTROL['port_access_check']:
            for portObj,macList in port_macList.items():
                if portObj.access != 0:  ## port access non switch
                    for mac in macList:
                        if mac in macDictKeys:
                            if macDict[mac].port != portObj:
                                macDict[mac].port = portObj
                                macDict[mac].save()
                        else:
                            models.Mac.objects.create(port=portObj,mac=mac)      
        else:                   ## non start define.port_access_check
            for portObj,macList in port_macList.items():
                if len(macList) < define.MaxMacPortNumber:
                    for mac in macList:
                        if mac in macDictKeys:
                            if macDict[mac].port != portObj:
                                macDict[mac].port = portObj
                                macDict[mac].save()
                        else:
                            models.Mac.objects.create(port=portObj,mac=mac)

        return True
             
        
    @decorate('command.default','getMac')
    def getMac(self,*args,**kwargs):
        switchObj = kwargs['switchObj']

        if switchObj.getMacControl & define.GET_MAC_CONTROL['standard_getMac'] == define.GET_MAC_CONTROL['standard_getMac']:
            kwargs['message'] = 'start standard_getMac';logger.info(**kwargs)
            self._standard_getMac(*args,**kwargs)
        else:
            kwargs['message'] = 'start non_standard_getMac';logger.info(**kwargs)
            self._non_standard_getMac(*args,**kwargs)
        return True
            
                
    @decorate('command','getsysDecr')
    def getsysDecr(self,*args,**kwargs):
        switchObj=kwargs['switchObj']

        switchObj.oidName = 'sysDecr'

        generic = self._command(**kwargs)
        if not generic:
            return None

        for key,value in generic.items():
            if len(value) > 220:
                value = value[0:219]
            switchObj.sysDecr = value

        switchObj.getData = switchObj.getData - GET_DATA[switchObj.get_data_function]
        switchObj.save()
        
        return True
    
    @decorate('command','makeDesc')
    def makeDesc(self,*args,**kwargs):
        switchObj = kwargs['switchObj']
        get_data   = switchObj.getData


        func_value = GET_DATA[ switchObj.get_data_function ]

        if not (get_data & func_value == func_value):
            kwargs['message'] = '    switch makeDesc  no start'; logger.info(**kwargs)
            return True


        oidNameList = ['dot1dBasePortIfIndex','ifName','dot1dTpFdbAddress','dot1dTpFdbPort','sysDecr']
        desc = ''
        for oidName in oidNameList:
            switchObj.oidName = oidName
            comClass,comFunc = base.get_class_func(model=oid,switchObj=switchObj)
            generic = comFunc(comClass(),switchObj=switchObj)

            try:
                desc = '%s%s generic number is %s\n' % (desc,oidName,len(generic))
            except:
                desc = '%s%s generic None\n' % (desc,oidName)

        switchObj.desc = desc
        switchObj.getData =  switchObj.getData - func_value
        switchObj.save()





class BaseNoSupportdot1dTpFdbAddress(Default,metaclass=base.metaclass):
    """有些交换机不支持oid:dot1dTpFdbAddress，相同型号不同Bin版本可能也有差异"""
    pass

class H3C_S3100V2_26TP_SI(BaseNoSupportdot1dTpFdbAddress,metaclass=base.metaclass):
    pass
