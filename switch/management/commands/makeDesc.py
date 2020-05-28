from django.core.management.base import BaseCommand, CommandError
import multiprocessing
import time

from switch import models
from switch import command
from switch import oid
from switch import base
from switch.base import decorate
from switch.define import *

from switch.log import logger

@decorate('makeDesc','desc')
def target(*args,**kwargs):

    switchObj=kwargs['switchObj']
    switchObj.get_data_function = 'makeDesc'
    kwargs['message'] = '   --------start %s:%s:%s-------' % (switchObj.name,switchObj.ip,switchObj.get_data_function);logger.info(**kwargs)
    comClass,comFunc = base.get_class_func(model=command,switchObj=switchObj)
    if comFunc:
        comFunc(comClass(),switchObj=switchObj)

    kwargs['message'] = '   --------end %s:%s:%s-------' % (switchObj.name,switchObj.ip,get_data_function);logger.info(**kwargs)
    print(kwargs['message'])
class Command(BaseCommand):
    def handle(self, *args, **options):
        
        pool = multiprocessing.Pool(processes = processNumber)

        switchS = models.Switch.objects.all()
        for switchObj in switchS:
            pool.apply_async(target,(),{'switchObj':switchObj})

        pool.close()
        pool.join()     
           
