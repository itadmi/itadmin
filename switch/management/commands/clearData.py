from django.core.management.base import BaseCommand, CommandError
import multiprocessing
import time

from switch import models
from switch import command
from switch import base
from switch.base import decorate,clear
from switch.define import *

from switch.log import logger


class Command(BaseCommand):
    def handle(self, *args, **options):
        base.clear() 
