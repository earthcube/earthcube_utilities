import sys
import json
def inCollab():
    """ Is this notebook being run in Goolge Collab"""
    return  'google.colab' in sys.modules

def get_txtfile(fn):
    "ret str from file"
    with open(fn, "r") as f:
        return f.read()

def get_jsfile2dict(fn):
    "get jsonfile as dict"
    #s=get_txtfile(fn)
    #return json.loads(s)
    with open(fn, "r") as f:
        return json.load(f)

def put_txtfile(fn,s,wa="w"):
    "filename to dump string to"
    #with open(fn, "w") as f:
    with open(fn, "a") as f:
        return f.write(s)