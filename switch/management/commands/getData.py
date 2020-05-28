from django.core.management.base import BaseCommand, CommandError
import multiprocessing
import time

from switch import models
from switch import command
from switch import base
from switch.base import decorate
from switch.define import *

from switch.log import logger

@decorate('getData','target')
def target(*args,**kwargs):

    switchObj=kwargs['switchObj']
    get_data_functions = ['initPort','getMac','getsysDecr','makeDesc']
    for get_data_function in get_data_functions:
        getData = switchObj.getData
        if ( getData & GET_DATA[get_data_function] == GET_DATA[get_data_function] ) and \
                     (getData & GET_DATA['enable'] == GET_DATA['enable']):         
            switchObj.get_data_function = get_data_function
            try:
                delattr(switchObj,'oidName')
            except:
                pass
    
            kwargs['message'] = '   --------start %s:%s:%s-------' % (switchObj.name,switchObj.ip,get_data_function);logger.info(**kwargs) 
            comClass,comFunc = base.get_class_func(model=command,switchObj=switchObj)
            if comFunc:
                comFunc(comClass(),switchObj=switchObj)
            kwargs['message'] = '   --------end %s:%s:%s-------' % (switchObj.name,switchObj.ip,get_data_function);logger.info(**kwargs)
        else:
            kwargs['message'] = '   --------%s:%s:%s,  no open -------' % (switchObj.name,switchObj.ip,get_data_function);logger.info(**kwargs)

class Command(BaseCommand):
    def handle(self, *args, **options):
        
        pool = multiprocessing.Pool(processes = processNumber)

        switchS = models.Switch.objects.all()
        for switchObj in switchS:
            pool.apply_async(target,(),{'switchObj':switchObj})

        pool.close()
        pool.join()     
           
