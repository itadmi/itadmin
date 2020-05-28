import logging
from logging.handlers import TimedRotatingFileHandler

import os,sys

from django.conf import settings



class Logger:
    def __init__(self,Flevel=logging.DEBUG):
        fmt = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s', '%Y-%m-%d %H:%M:%S')

        logfile_name =os.path.join(settings.BASE_LOG,'log')
        time_rotate_file = TimedRotatingFileHandler(filename=logfile_name, when='D', interval=1, backupCount=2)
        time_rotate_file.setFormatter(fmt)
        time_rotate_file.setLevel(Flevel)

        self.logger=logging.getLogger(logfile_name)
        self.logger.addHandler(time_rotate_file)
        self.logger.setLevel(Flevel)

    def _message(self,**kwargs):
        try:
            switchObj = kwargs['switchObj']
        except:
            pass

        try:
            base_message = '[%s]' % switchObj.name
        except:
            base_message = ''

        try:
            base_message = "%s[%s]" % (base_message,switchObj.get_data_function)
        except:
            pass
        try:
            base_message = "%s   [%s]" % (base_message,switchObj.oidName)
        except:
            base_message = "%s   " % base_message

        try:
            base_message = '%s[%s]' % ( base_message ,kwargs['modelName'])
        except:
            pass

        try:
            base_message = '%s:[%s]' %   (base_message, kwargs['funcName'])
        except:
            pass

        return base_message

    def info(self,**kwargs):
        base_message = self._message(**kwargs)
        message = "%s   ###  %s" % (base_message,kwargs['message'])
        self.logger.info(message)

    def error(self,**kwargs):
        base_message = self._message(**kwargs)
        message = "%s  !!!!  %s" % (base_message,kwargs['message'])
        self.logger.error(message)



class SwitchLog():
    pass

switchObj = SwitchLog()
switchObj.taskNumber = '1002'
switchObj.name = 'HR01'
switchObj.ip = '172.16.170.1'
switchObj.type  = 'Default'
switchObj.community = 'public'
switchObj.oidValue  = 'ifDescr'

switchObj.taskFlag = 'switch:ifDescr'

logger = Logger()
