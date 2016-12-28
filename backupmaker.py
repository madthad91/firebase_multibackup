#this source requires pip install pyyaml
import urllib2, json, datetime, yaml, setInterval

backup_interval = 10 # in seconds
yamldata = -1
def overrideGeneral():
    try:
        backup_interval = yamldata["General"]["interval"]
    except Exception as e:
        print(str("No general interval set. Moving on.."))

def makebackup(host, key, outname):
    url = 'https://'+ host + '.firebaseio.com/.json?format=export&auth='+key
    print("data summary", host, key,outname, url)
    resp = urllib2.urlopen(url)
    json_obj = json.load(resp)
    #python's open definition of open: file object = open(file_name [, access_mode][, buffering])
    #w+ gives read and write functionality
    new_backup = open('backups/'+ datetime.datetime.now().strftime("(%Y-%m-%d)_@%Ith hour %Mmins %Ssecs %p")+'.json', 'w+')
    new_backup.write(json.dumps(json_obj))#, sort_keys=True, indent=2, separators=(',', ': '))) #the extra code is to enable pretty printing which takes up more space
    new_backup.close()

with open("firebase_backups.yaml", 'r') as stream:
    try:
        yamldata = yaml.load(stream)
        keyset = yamldata.keys()
        if "General" in yamldata:
            overrideGeneral()
            del keyset[keyset.index("General")]
        for key in keyset:
            try:
                yamldata[key]["secret_key"]
            except yaml.YAMLError as exc:
                print(exc)
            
            # per firebase db, extract an override interval
            temp_interval = -1
            if "interval" in yamldata[key]:
                temp_interval = yamldata[key]["interval"]
            else:
                temp_interval = backup_interval

            #run setInterval    
            setInterval(makebackup(key, yamldata[key]["secret_key"], yamldata[key]["output_name"]), temp_interval) #pyton equivalent to javascript's setInterval
            print(key +" is in the keyset")
    except yaml.YAMLError as exc:
        print(exc)