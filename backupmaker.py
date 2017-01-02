#!/usr/bin.env python
''' this source requires pip install pyyaml
    __sample__ = 3  a proposed way of avoiding the all caps rule'''
import os
import urllib2
import json
import datetime
import socket
import yaml
import set_interval

HOST, PORT = '', 8888

class FirebaseBackupper(object):
    """ this is a sample docstring """
    def __init__(self):
        self.backupinterval = 10 #in seconds
        self.yamldata = {}
        self.runner()
    def overridegeneral(self):
        '''the override general function '''
        try:
            self.backupinterval = self.yamldata["General"]["interval"]
        except yaml.YAMLError:
            print str("No general interval set. Moving on..")
    def makebackup(self, *args):
        ''' this is the method to make a function '''
        if len(args) == 0:
            print 'not enough arguments'
            return
        print args
        host = args[0]
        if not host:
            print 'Hostname not specified. exiting...'
            return
        key = args[1]
        if not key:
            print 'Secret key not specified. exiting...'
            quit()
        outname = args[2]
        if not outname:
            outname = key
        url = 'https://'+ host + '.firebaseio.com/.json?format=export&auth='+key
        print "data summary", host, key, outname, url
        resp = urllib2.urlopen(url)
        json_obj = json.load(resp)
        #python's open definition of open:file object = open(file_name [, access_mode][, buffering])
        #w+ gives read and write functionality
        dest_file = "backups"
        if outname:
            dest_file = outname
        if not os.path.exists(dest_file+'/'):
            os.makedirs(dest_file+'/')
        dateformat = "(%Y-%m-%d)_@%Ith hour %Mmins %Ssecs %p"
        new_backup = open(dest_file+'/'+
                          datetime.datetime.now().strftime(dateformat)+
                          '.json', 'w+')
        new_backup.write(json.dumps(json_obj))#, sort_keys=True, indent=2, separators=(',', ': ')))
        #the extra code above in the comment is to enable pretty printing which takes up more space
        new_backup.close()
    def runner(self):
        ''' the backup programs runner '''
        with open("firebase_backups.yaml", 'r') as stream:
            try:
                self.yamldata = yaml.load(stream)
                print self.yamldata
                keyset = self.yamldata.keys()
                if "General" in self.yamldata:
                    self.overridegeneral()
                    del keyset[keyset.index("General")]
                for key in keyset:
                    try:
                        self.yamldata[key]["secret_key"]
                    except yaml.YAMLError as exc:
                        print(exc, "The secret key is a required field. exiting...")
                        quit()
                    # per firebase db, extract an override interval
                    temp_interval = -1
                    if "interval" in self.yamldata[key]:
                        temp_interval = self.yamldata[key]["interval"]
                    else:
                        temp_interval = self.backupinterval

                    #run setInterval
                    set_interval.set_interval(self.makebackup, temp_interval, key,
                                              self.yamldata[key]["secret_key"]
                                              if "secret_key" in self.yamldata[key] else None,
                                              self.yamldata[key]["output_name"]
                                              if "output_name" in self.yamldata[key]  else None)
                                              #pyton equivalent to javascript's setInterval
                    print key + " is in the keyset"
            except yaml.YAMLError as exc:
                print exc

def webserver():
    ''' the server to fetch backups '''
    print 'hey thad'
    listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listen_socket.bind((HOST, PORT))
    listen_socket.listen(1)
    print 'Serving HTTP on port %s ...' % PORT
    # while True:
    #     client_address, client_connection = listen_socket.accept()
    #     print client_address
    #     request = client_connection.recv(1024)
    #     print request

    #     http_response = """
    #       HTTP/1.1 200 OK

    #       Hello, World!
    #       """
    #     client_connection.sendall(http_response)
    #     client_connection.close()

if __name__ == "__main__":
    webserver()
    FirebaseBackupper()
    # def main():
    #     ''' main function def '''
    #     hai = Hai()
    #     hai.runner()
    # main()
