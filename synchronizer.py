import os, time
from syncData.APIExtract import *
from syncData.SyncDb import *
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Funx.settings")

django.setup()

cache = ''

if __name__ == '__main__':
    while True:
        response = APIExtract().connect()
        '''
        if confirmDifferences(response, cache):
            updateDatabase(response)
        cache = response
        '''
        print('hola')
        time.sleep(nextIteration())
