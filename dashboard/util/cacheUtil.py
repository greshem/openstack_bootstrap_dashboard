# -*- coding: utf-8 -*-
'''
Created on 2016年11月16日

@author: zzg
'''
import time
import hashlib
import pickle

cache = {}

def _is_obsolete(entry):
    d = time.time() - entry['time']
    return d >= entry['duration']

def add_cache(name, result, duration=60):
    key = hashlib.sha1(pickle.dumps(name)).hexdigest()
    cache[key] = { 'value':result, 'time':time.time(), 'duration': duration}

def get_cache(name):
    key = hashlib.sha1(pickle.dumps(name)).hexdigest()
    if key in cache and not _is_obsolete(cache[key]):
        return cache[key]['value']
    return None