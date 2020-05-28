import sys,os,time,shutil,time
from functools import wraps
from configparser import ConfigParser
from django.conf import settings
from switch.log import logger
from switch import define
from datetime import datetime

try:
    from pysnmp.entity.rfc3413.oneliner import cmdgen
except Exception:
    print("You need to install pysnmp and pyasn1")
    sys.exit(1)



class Config(object):
    def __init__(self,**kwargs):
        try:            
            cf = settings.CF

            cp  = ConfigParser()
            cp.read(cf)
            self.sections = cp.sections()
            self.options  = {}
            for section in self.sections:
                items = cp.items(section)
                self.options[section] = {}
                for item in items:
                    tmp =tuple([int(i) for i in item[1].split('.')])
                    self.options[section][item[0]] = tmp
        except:
            ##logger.error(switchObj=switchObj,function=function,message='No this Config File:%s' % cf)
            sys.exit(1)  

cf = Config()

def getDhcpConfig():
    mssql = settings.MSSQL
    cp  = ConfigParser()
    try:
        cp.read(mssql)
        host = cp.get('msdb','host')
        user = cp.get('msdb','user')
        password = cp.get('msdb','password')
        database = cp.get('msdb','database')
        return host,user,password,database
    except:
        sys.exit(1)



def get_SwType():
    """ define.swType"""
    sections = cf.sections
    if len(sections) == 0:
        return ()
    n = 0
    SwType =[]
    for section in sections:
        tmpList = [n]
        tmpList.append(section)
        tmpTuple = tuple(tmpList)
        SwType.append( tmpTuple)
        n = n +1
    return tuple(SwType)




def decorate(modelName,funcName):
    def log(func):
        @wraps(func)
        def wrapper( *args,**kwargs):
            kwargs['modelName'] = modelName
            kwargs['funcName']  = funcName
            kwargs['message']   = 'start: %s--%s' % (modelName,funcName); logger.info(**kwargs)

            retValue = func(*args,**kwargs)

            kwargs['message']   = 'end : %s--%s' % (modelName,funcName);logger.info(**kwargs)

            return retValue
        return wrapper
    return log



@decorate('base','get_oid_str')
def get_oid_str(*args,**kwargs):
    switchObj = kwargs['switchObj']
    oidName   = switchObj.oidName.lower()        ##configparser options  default lower
    function = 'base.get_oid_str'
    switch_type = cf.sections[switchObj.type]
    try:
        oidStr = cf.options[switch_type][oidName]
        kwargs['message'] = 'oidName:%s switch_type:%s get oid_str:%s' % (oidName,switch_type,oidStr)
        logger.info(**kwargs)
        return oidStr

    except:
        try:
            oidStr = cf.options['Default'][oidName]
            kwargs['message'] = 'oidName:%s No switch_type:%s Default Class get oid_str:%s' % (oidName,switch_type,oidStr)
            logger.info(**kwargs)
            return oidStr
        except:
            kwargs['message'] = 'no oidName:%s in class !!%s and Default!!' % (oidName,switch_type)
            logger.error(**kwargs)
            return None
    


@decorate('base','walk')
def walk(*args,**kwargs):
    switchObj = kwargs['switchObj']
    community = switchObj.community
    ip        = switchObj.ip
    oidValue       = get_oid_str(*args,**kwargs)
    
    if not oidValue:
        kwargs['message'] ='call get_oid_str return None, so base.walk return None'
        logger.error(**kwargs)
        return None
    
    errorIndication, errorStatus, errorIndex, \
        generic = cmdgen.CommandGenerator().nextCmd(cmdgen.CommunityData('test-agent', community), \
                                  cmdgen.UdpTransportTarget((ip, 161)),oidValue,ignoreNonIncreasingOid=True)
    
    if not generic:
        ## the switch no the Oid
        kwargs['message'] = 'The Switch:%s not support thd Oid:%s return None' % (switchObj.name,switchObj.oidName) 
        logger.error(**kwargs)

    try:
        number = len(generic)
        kwargs['message'] = 'Oid:%s base.walk  return generic recoder number:[%s]' % (switchObj.oidName,number)
        logger.info(**kwargs)
    except:
        kwargs['message'] = 'oid:%s len(generic) fault,unknow walk generic number' % switchObj.oidName
        logger.error(**kwargs)

    return generic


@decorate('base','get_class_fuc')
def get_class_func(*args,**kwargs):
    model       = kwargs['model']
    switchObj   = kwargs['switchObj']
    switch_type = cf.sections[switchObj.type]
    try:
        oidName     = switchObj.oidName
    except:
        oidName     = switchObj.get_data_function

    try:
        class_name = model.__dict__[switch_type]
    except:
        try:
            class_name = model.__dict__['Default']
        except:
            kwargs['message'] = 'in model:%s No Default class And no :%s,return None' % (model.__name__,switch_type )
            logger.error(**kwargs)
            return None,None

    try:
        func  = class_name.Func[oidName]
    except:
        try:
            func = model.__dict__['Default'].Func[oidName]
        except:
            kwargs['message'] = '   %s.Default No function:%s' % ( model.__name__,oidName)
            logger.error(**kwargs)
            return None,None

    kwargs['message'] = 'reutrn class:func  --> %s:%s' % (class_name.__name__,func.__name__)
    logger.info(**kwargs)


    return class_name,func
    


def metaclass(future_class_name, future_class_parents, future_class_attrs):
    attrs = {}
    attrs["Func"] = {}

    for k, v in future_class_attrs.items():
        attrs[k] = v
        if k == '__module__' or k == '__qualname__':
            continue
        if isinstance(v, type(lambda _: _)):
            attrs["Func"][k] = v

    return type(future_class_name, future_class_parents, attrs)


@decorate('base','make_file_name')
def make_file_name(**kwargs):
    ##/../DATA/switch_name/taskNumber
    switchObj = kwargs['switchObj']
    oidName   = switchObj.oidName
    name = switchObj.name


    localtime =time.localtime()
    taskNumber = '%s-%s-%s-%sHour-%s-%s'% (localtime.tm_year,localtime.tm_mon,localtime.tm_mday,localtime.tm_hour,localtime.tm_min,localtime.tm_sec)
    path = os.path.join(settings.BASE_OID,name)
    if not os.path.exists(path):
        os.mkdir(path)
    fileName = os.path.join(path,'%s-%s' % (oidName,taskNumber))
    if os.path.exists(fileName):
        fileNameMove = "%s.%s"  % ( fileName, int(time.time()))
        shutil.move(fileName,fileNameMove)
    kwargs['message'] = 'Return fileName:%s'  % fileName
    logger.info(**kwargs)
    return fileName


@decorate('base','make_file_name_DEBUG')
def make_file_name_DEBUG(**kwargs):
    localtime =time.localtime()
    taskNumber = 'Year%s-Month%s-Day%s-Hour%s-Min%s-Sec%s'% \
            (localtime.tm_year,localtime.tm_mon,localtime.tm_mday,localtime.tm_hour,localtime.tm_min,localtime.tm_sec)
    path = settings.BASE_DEBUG
    if not os.path.exists(path):
        os.mkdir(path)

    fileName = os.path.join(path,'%s' % taskNumber)
    kwargs['message'] = 'Return fileName:%s'  % fileName
    logger.info(**kwargs)
    return fileName


def clear():
    curTime = time.time()
    path = settings.BASE_OID
    remove = define.REMOVE_FILE * 86400
    walks = os.walk(path)
    for walk in walks:
        if walk[2]:
            for f in walk[2]: 
                fileName =  os.path.join(walk[0],f)
                ctime = os.path.getctime(fileName)
                if curTime  > ctime + remove :
                    try:
                        os.remove(fileName)
                    except:
                        pass


