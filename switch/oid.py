
from switch import base
from switch.base import decorate
from switch.log import logger
from switch import deal

class Default(metaclass=base.metaclass):
    def __init__(self,**kwargs):
        """call: ifdescr =oidObj.ifDescr(model=deal,oidName='ifDescr',switchObj=switchObj)"""
        self.sections = base.cf.sections
        
    @decorate('oid','_default')
    def _default(self,*args,**kwargs):
    
        switchObj=kwargs['switchObj']
        oidName  = switchObj.oidName

        generic = base.walk(oidName = oidName,switchObj= switchObj)
        if not generic:
            return None
        ############# generic change to dict ##############################
        
        #get class ,func
        dealClass,dealFunc = base.get_class_func(model=deal,switchObj=switchObj)

        if not dealFunc:
            switch_type = self.sections[switchObj.type]
            kwargs['message'] = 'Switch.oid.%s.%s no funC' % (switch_type,oidName)
            logger.error(**kwargs)
            return None

        ## deal with generic
        dealObj = dealClass()
        retDict = dealFunc(dealObj,model=deal,switchObj=switchObj,generic=generic)
        return retDict


    @decorate('oid','ifDescr')
    def ifDescr(self,*args,**kwargs):
        retDict =  self._default(*args,**kwargs)     

        return retDict


    @decorate('oid','dot1dBasePortIfIndex')
    def dot1dBasePortIfIndex(self,*args,**kwargs):
        retDict =  self._default(*args,**kwargs)
        return retDict


    @decorate('oid','ifName')
    def ifName(self,*args,**kwargs):
        retDict =  self._default(*args,**kwargs)
        return retDict


    @decorate('oid','dot1dTpFdbAddress')
    def dot1dTpFdbAddress(self,*args,**kwargs):
        retDict =  self._default(*args,**kwargs)
        return retDict


    @decorate('oid','dot1dTpFdbPort')
    def dot1dTpFdbPort(self,*args,**kwargs):
        retDict =  self._default(*args,**kwargs)
        return retDict



    @decorate('oid','ipNetToMediaPhysAddress')
    def ipNetToMediaPhysAddress(self,*args,**kwargs):
        """ip map mac-addrss == iso.3.6.1.2.1.4.22.1.2.18729.172.16.30.38 = Hex-STRING: C0 9F 05 A0 B5 3D"""
        retDict =  self._default(*args,**kwargs)
        return retDict

    @decorate('oid','sysDecr')
    def sysDecr(self,*args,**kwargs):
        retDict =  self._default(*args,**kwargs)
        return retDict


class H3C(Default,metaclass=base.metaclass):
    pass
