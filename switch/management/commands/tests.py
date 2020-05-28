from django.core.management.base import BaseCommand, CommandError
import multiprocessing
import time

from switch import models,oid,command
from switch import tests
from switch import base

from switch.define import *



def target(switchObj):
        
    pass
class Command(BaseCommand):
    def handle(self, *args, **options):
        
        tests.test_sysDecr() 
