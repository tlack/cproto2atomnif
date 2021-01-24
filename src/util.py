import sys

def die(msg):
    print(msg)
    sys.exit(1)

def warn(msg):
    if type(msg) == type([]):
        msg = " ".join(msg)
    print('WARNING:', warn)
    
