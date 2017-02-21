import sys
from django.core.management.base import BaseCommand
import time

sys.path.append('../../')
from constructModelForGunosy import *


#The class must be named Command, and subclass BaseCommand
class Command(BaseCommand):
    help = "Test training function"

    # A command must define handle()
    def handle(self, *args, **options):
        print("Testing the training function of MultivariateBernoulli.py")
        start_time = time.time()
        train_with_all_data()
        print("--- %s seconds --- spent in training data" % (time.time() - start_time))
        print("the model is saved as example.pickle in data/")
