#this source requires pip install pyyaml
import os, urllib2, json, datetime, yaml
from setInterval import *

backup_interval = 10 # in seconds
yamldata = -1
def overrideGeneral():
    try:
        backup_interval = yamldata["General"]["interval"]
    except Exception as e:
        print(str("No general interval set. Moving on.."))

def makebackup(*args):
    if len(args) == 0:
        print('not enough arguments')
        return
    print(args)
    host = args[0]
    if not host:
        print('Hostname not specified. exiting...')
        return
    key = args[1]
    if not key:
        print('Secret key not specified. exiting...')
        quit()
    outname = args[2]
    if not outname:
        outname = key
    url = 'https://'+ host + '.firebaseio.com/.json?format=export&auth='+key
    print("data summary", host, key,outname, url)
    resp = urllib2.urlopen(url)
    json_obj = json.load(resp)
    #python's open definition of open: file object = open(file_name [, access_mode][, buffering])
    #w+ gives read and write functionality
    dest_file = "backups"
    if outname:
        dest_file = outname
    if not os.path.exists(dest_file+'/'):
        os.makedirs(dest_file+'/')
    new_backup = open(dest_file+'/'+ datetime.datetime.now().strftime("(%Y-%m-%d)_@%Ith hour %Mmins %Ssecs %p")+'.json', 'w+')
    new_backup.write(json.dumps(json_obj))#, sort_keys=True, indent=2, separators=(',', ': '))) #the extra code is to enable pretty printing which takes up more space
    new_backup.close()

with open("firebase_backups.yaml", 'r') as stream:
    try:
        yamldata = yaml.load(stream)
        print(yamldata)
        keyset = yamldata.keys()
        if "General" in yamldata:
            overrideGeneral()
            del keyset[keyset.index("General")]
        for key in keyset:
            try:
                yamldata[key]["secret_key"]
            except yaml.YAMLError as exc:
                print(exc, "The secret key is a required field. exiting...")
                quit()
            
            # per firebase db, extract an override interval
            temp_interval = -1
            if "interval" in yamldata[key]:
                temp_interval = yamldata[key]["interval"]
            else:
                temp_interval = backup_interval

            #run setInterval
            setInterval(makebackup, temp_interval, key, 
                yamldata[key]["secret_key"] if "secret_key" in yamldata[key]  else None, 
                yamldata[key]["output_name"] if "output_name" in yamldata[key]  else None) #pyton equivalent to javascript's setInterval
            print(key +" is in the keyset")
    except yaml.YAMLError as exc:
        print(exc)