from django.test import TestCase
import time
from switch import command
from switch import models
from switch import base
from switch import oid
# Create your tests here.


from switch.base import decorate
from switch.log import logger
def ifdescr(**kwargs):
    com = command.Command()
    print('test')
    com.ifDescr(switchObj=switchObj,oidName=oidName)

def descrCom():
    switchObj = models.Switch.objects.get(ip='172.16.170.1')
    oidName= 'ifDescr'
    ifdescr(switchObj=switchObj,oidName=oidName)


def test_get_oid_str():
    switchObj = models.Switch.objects.get(ip='172.16.170.1')
    switchObj.taskNumber = 21111
    switchObj.oidName = 'ifDescr'
    oidName= 'ifDescr'
    return base.get_oid_str(switchObj=switchObj,oidName=oidName)

def test_oid_ifDescr():
    switchObj = models.Switch.objects.get(ip='172.16.170.4')
    switchObj.taskNumber = 21111
    oidName= 'ifDescr'

    switchObj.taskNumber = 22222
    oidClass,oidFunc = base.get_class_func(model=oid,switchObj=switchObj,oidName=oidName)
    return oidFunc(oidClass(),switchObj=switchObj,oidName=oidName)
def test_com_dot1dBasePortIfIndex():
    switchObj = models.Switch.objects.get(ip='172.16.150.6')
    switchObj.taskNumber = 4444
    switchObj.oidName = 'dot1dBasePortIfIndex'
    oidName= 'dot1dBasePortIfIndex'

    comClass,comFunc = base.get_class_func(model=command,switchObj=switchObj,oidName=oidName)
    comFunc(comClass(),switchObj=switchObj,oidName=oidName)

def test_com_ifName():
    switchObj = models.Switch.objects.get(ip='172.16.150.6')
    switchObj.taskNumber = 33333
    switchObj.oidName = 'ifName'
    oidName= 'ifName'

    comClass,comFunc = base.get_class_func(model=command,switchObj=switchObj,oidName=oidName)
    if not comFunc:
        print('comFunc')
    if not comClass:
        print('comClass')
    try:
        comClass()
    except:
        print('comClass')
    comFunc(comClass(),switchObj=switchObj,oidName=oidName)



def test_com_ifDescr():
    switchObj = models.Switch.objects.get(ip='172.16.150.6')
    switchObj.taskNumber = 4444
    switchObj.oidName = 'ifDescr'
    oidName= 'ifDescr'

    comClass,comFunc = base.get_class_func(model=command,switchObj=switchObj,oidName=oidName)
    comFunc(comClass(),switchObj=switchObj,oidName=oidName)

def test_com_dot1dTpFdbAddress():
    switchObj = models.Switch.objects.get(ip='172.16.170.1')
    switchObj.taskNumber = 33333
    switchObj.oidName = 'dot1dTpFdbAddress'
    oidName= 'dot1dTpFdbAddress'

    comClass,comFunc = base.get_class_func(model=command,switchObj=switchObj,oidName=switchObj.oidName)
    return comFunc(comClass(),switchObj=switchObj,oidName=switchObj.oidName)


def test_command_initPort():
    switchObj = models.Switch.objects.get(ip='172.16.150.6')
    functionName = 'initPort'
    switchObj.oidName = functionName
    comClass,comFunc = base.get_class_func(model=command,switchObj=switchObj)
    comFunc(comClass(),switchObj=switchObj)

def test_com_version():
    switchObj = models.Switch.objects.get(ip='172.16.170.1')
    switchObj.oidName = 'version'
    switchObj.versionModel = 'version'
    switchObj.getData = 31
    switchObj.get_data_function = 'getVersion'

    comClass,comFunc = base.get_class_func(model=command,switchObj=switchObj)
    comFunc(comClass(),switchObj=switchObj)



@decorate('modelName','functionName')
def test_logger2(*args,**kwargs):
    message='test_logger2'
    kwargs['message'] = message
    logger2.info(*args,**kwargs)
    logger2.error(*args,**kwargs)
    return 
def test_walk():
    oidName = 'sysDecr'
    switchObj = models.Switch.objects.get(ip='172.16.170.1')
    switchObj.oidName = oidName
    generic = base.walk(switchObj=switchObj)
    return generic



def tests_initPort():
    switchObj = models.Switch.objects.get(ip='172.16.150.6')
    switchObj.oidName = 'initPort'

    comm = command.Default()
    comm.initPort(switchObj=switchObj)

def test_getMac():
    switchObj = models.Switch.objects.get(ip='172.16.170.2')
    switchObj.get_data_function = 'getMac'
    comClass,comFunc = base.get_class_func(model=command,switchObj=switchObj)
    print(comClass.__name__)
    return comFunc(comClass(),switchObj=switchObj)

def test_sysDecr():
    switchObj = models.Switch.objects.get(ip='172.16.140.254')
    switchObj.get_data_function = 'getsysDecr'
    comClass,comFunc = base.get_class_func(model=command,switchObj=switchObj)
    print(comClass.__name__)
    if comFunc:
        return comFunc(comClass(),switchObj=switchObj)

def test_initPort():
    switchSet = models.Switch.objects.all()
    oidNameList = ['dot1dBasePortIfIndex','ifName']

    for switchObj in switchSet:
        for oidName in oidNameList:
            switchObj.oidName = oidName
            comClass,comFunc = base.get_class_func(model=oid,switchObj=switchObj)
            generic = comFunc(comClass(),switchObj=switchObj)
            try:
                if len(generic) == 0:
                    print('name:%s oidName:%s generic is None' % (switchObj.name,oidName))
            except:
                print('name:%s oidName:%s generic is None' % (switchObj.name,oidName))

                
def test_getMaci():
    switchSet = models.Switch.objects.all()
    oidNameList = ['dot1dTpFdbAddress','dot1dTpFdbPort']
    for switchObj in switchSet:
        for oidName in oidNameList:
            switchObj.oidName = oidName
            comClass,comFunc = base.get_class_func(model=oid,switchObj=switchObj)
            generic = comFunc(comClass(),switchObj=switchObj)
            try:
                if len(generic) == 0:
                    print('name:%s oidName:%s generic is None' % (switchObj.name,oidName))
            except:
                print('name:%s oidName:%s generic is None' % (switchObj.name,oidName))
                


