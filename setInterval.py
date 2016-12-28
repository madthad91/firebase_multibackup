import threading

def setInterval(func,time, a, b, c):
    e = threading.Event()
    while not e.wait(time):
        print('before the func call')
        func(a, b, c)