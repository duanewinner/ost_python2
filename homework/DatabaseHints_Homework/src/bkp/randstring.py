# Return a random gen. all-char string -- useful for tmp db tables.
import random

def randstring(length=16):
    rletters='abcdefghijklmnopqrstuvwxyz'
    return ''.join((random.choice(rletters) for i in range(length)))
