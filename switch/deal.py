from switch import base
from switch.base import decorate
from switch.log import logger

class Default(metaclass=base.metaclass):
    def __init__(self,**kwargs):
        self.sections = base.Config().sections
    

    @decorate('deal','ifDescr')
    def ifDescr(self,**kwargs):
        switchObj = kwargs['switchObj']
        generic = kwargs['generic']
        retValue = {}
        fileName = base.make_file_name(switchObj=switchObj)
        with open(fileName,'a') as f:
            for line in generic:
                try:
                    line0 = line[0]
                    value = str(line[0][1])
                    key = int(line[0][0][-1])
                    print(key)
                    f.write('%s change to %s:%s\n' %(str(line0),key,value))
                    retValue[key]=value
                    print(value)
                except:
                    f.write('%s change to error\n' %str(line0))

        return retValue

    @decorate('deal','dot1dBasePortIfIndex')
    def dot1dBasePortIfIndex(self,**kwargs):
        """SNMPv2-SMI::mib-2.17.1.4.1.2.1 = 1"""

        switchObj = kwargs['switchObj']
        generic = kwargs['generic']
        retValue = {}
        fileName = base.make_file_name(switchObj=switchObj)

        with open(fileName,'a') as f:
            for line in generic:
                try:
                    line0 = line[0]
                    key = line[0][0][-1]
                    value = line[0][1]
                    f.write('%s change to %s:%s\n' %(str(line0),key,value))
                    retValue[key]=value
                except:
                    f.write('%s change to error\n' %str(line0))

        return retValue
    @decorate('deal','ifName')
    def ifName(self,**kwargs):
        switchObj = kwargs['switchObj']
        generic = kwargs['generic']
        retValue = {}
        fileName = base.make_file_name(switchObj=switchObj)
        with open(fileName,'a') as f:
            for line in generic:
                try:
                    line0 = line[0]
                    key   = line[0][0][-1]
                    value = str(line[0][1])
                    f.write('%s change to %s:%s\n' %(str(line0),key,value))
                    retValue[key]=value
                except:
                    pass

        return retValue

    @decorate('deal','dot1dTpFdbAddress')
    def dot1dTpFdbAddress(self,**kwargs):
        """SNMPv2-SMI::mib-2.17.4.3.1.1.0.80.86.132.173.237 = 0x00505684aded"""
        switchObj = kwargs['switchObj']
        generic = kwargs['generic']
        retValue = {}
        fileName = base.make_file_name(switchObj=switchObj)
        with open(fileName,'a') as f:
            for line in generic:
                try:
                    line0 = line[0]
                    key   = line[0][0][-6],line[0][0][-5],line[0][0][-4],line[0][0][-3],line[0][0][-2],line[0][0][-1]
                    value = line[0][1].asNumbers() ##0x00505684aded change (0,80,86,132,173,237)
                    f.write('%s change to %s:%s\n' %(str(line0),key,value))
                    key = mac_change_str(key);value = mac_change_str(value)
                    retValue[key]=value
                except:
                    pass
        return retValue
        

    @decorate('deal','dot1dTpFdbPort')
    def dot1dTpFdbPort(self,**kwargs):
        """SNMPv2-SMI::mib-2.17.7.1.2.2.1.2.1.0.80.86.132.173.237 = 26"""
        switchObj = kwargs['switchObj']
        generic = kwargs['generic']

        fileName = base.make_file_name(switchObj=switchObj)
        retValue = {}
        with open( fileName,'a') as f:
            for line in generic:
                try:
                    line0 =line[0]
                    try:
                        key   = line[0][0][-6],line[0][0][-5],line[0][0][-4],line[0][0][-3],line[0][0][-2],line[0][0][-1]
                        value = int(line[0][1])
                    except:
                        print('name:%s %s Error'%(switchObj.name,str(line0)))
                    f.write('%s change to %s:%s\n' %(str(line0),key,value))
                    key = mac_change_str(key)
                    retValue[key]=value
                except:
                    ##f.write('%s change to %s:%s\n' %(str(line0),key,value))
                    pass
        return retValue   

    @decorate('deal','ipNetToMediaPhysAddress')
    def ipNetToMediaPhysAddress(self,**kwargs):
        switchObj = kwargs['switchObj']
        generic = kwargs['generic']
        
        ###   deal generic ,write fileName
        ipMacDict = {}
        fileName = base.make_file_name(switchObj=switchObj)

        with open( fileName,'a') as f:
            for g in generic:
                tmpLine = str(g[0])
                ipStr = g[0][0]; macH = g[0][1]
                tmp = []
                for i in macH:
                    s = '%s' % hex(i)
                    if i < 16: tmp.append(s.replace('0x','0'))
                    else:      tmp.append(s.replace('0x',''))
                mac = ''.join(tmp)
                ip ='%s.%s.%s.%s' % (ipStr[-4],ipStr[-3],ipStr[-2],ipStr[-1])
                line = '%s change to:%s = %s\n' % (tmpLine,ip,mac)
                f.write(line)
                ipMacDict[ip]=mac
        return ipMacDict

    @decorate('deal','sysDecr')
    def sysDecr(self,**kwargs):
        switchObj = kwargs['switchObj']
        generic = kwargs['generic']
        versionDict = {}
        fileName = base.make_file_name(switchObj=switchObj)
        with open( fileName,'a') as f:
            key = 0
            value = ''
            for g in generic:
                try:
                    value = value + str(g[0][1]).replace('\r',' ').replace('\n','  ')
                except:
                    kwargs['message'] = 'value = value + str(g[0][1]).  IS ERROR'
                    logger.error(**args)
            line = '%s\n' % value
            f.write(line)
            versionDict[key] = value

        return versionDict

class H3C(Default):
    pass

def mac_change_str(mac): #(0, 80, 86, 132,237,173)
    try:
        tmpList = []
        for m in mac:
            s = '%s' % hex(m)
            if m < 16: tmpList.append(s.replace('0x','0'))
            else:      tmpList.append(s.replace('0x',''))
        retValue = ''.join(tmpList)
        return retValue
    except:
        return mac

