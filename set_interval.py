#!/usr/bin.env python
''' abstracting this helper function to a new file '''
import threading

def set_interval(func, time, firebase_endpoint, secret_key, output_name):
    '''duplicate setInterval from javascript '''
    evt = threading.Event()
    while not evt.wait(time):
        print 'before the func call'
        func(firebase_endpoint, secret_key, output_name)
