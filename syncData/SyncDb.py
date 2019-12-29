import hashlib
from datetime import datetime
import json
import django


def nextIteration():
    now = datetime.now()
    tomorrow = now.replace(hour=23, minute=0, second=0, microsecond=0)
    return (tomorrow - now).total_seconds()


def confirmDifferences(new_dict, old_dict):
    new = hashlib.sha1(new_dict.encode('utf-8')).hexdigest()
    old = hashlib.sha1(old_dict.encode('utf-8')).hexdigest()
    return new != old


def updateDatabase(new_data):
    dict=json.loads(new_data)

    pass
