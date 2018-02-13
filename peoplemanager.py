import os
import requests
import json
import argparse
import urllib
from colored import fg, attr

os.system("clear")

def banner():
    print("\t{}{}_____                 _        __  __                                   ".format(attr(1), fg('red')))
    print("\t    |  __ \               | |      |  \/  |                                  ")
    print("\t    | |__) |__  ___  _ __ | | ___  | \  / | __ _ _ __   __ _  __ _  ___ _ __ ")
    print("\t    |  ___/ _ \/ _ \| '_ \| |/ _ \ | |\/| |/ _` | '_ \ / _` |/ _` |/ _ \ '__|")
    print("\t    | |  |  __/ (_) | |_) | |  __/ | |  | | (_| | | | | (_| | (_| |  __/ |   ")
    print("\t    |_|   \___|\___/| .__/|_|\___| |_|  |_|\__,_|_| |_|\__,_|\__, |\___|_|   ")
    print("\t                    | |                                        _/ |          ")
    print("\t                    |_|                                      |___/           {}".format(attr('reset')))
    print("{} Version : 0.1 {} ".format(fg(183), attr('reset')))
    print("{} Daniel Vargas {} ".format(fg(226), attr('reset')))


def miproperties():
    xml = requests.get(args.domain + 
    '/_api/sp.userprofiles.peoplemanager/getmyproperties', 
    cookies=cookies, verify=False, headers = headers)
    data = json.loads(xml.text)
    return data
def printdata(data):
    if "error" in data:
       print("{} Error: {} {}".format(fg('red'), data["error"]["message"]["value"].encode('utf-8'), attr('reset'))) 
    else:
        usuario = data["d"]
        print("{}*******************************************************************{}".format(fg(190), attr('reset')))
        for u in usuario:
            if type(usuario[u]) is unicode:
                print("{}{}{} : {}".format(fg('green'), u,attr('reset'),  usuario[u].encode('utf-8')))
        print("{}*******************************************************************{}".format(fg(190), attr('reset')))

def finduser(user):
    print("Buscando usuario %s" % user)
    xml = requests.get(args.domain + 
    '/_api/sp.userprofiles.peoplemanager/getpropertiesfor(@v)?@v=' + 
    user,
    cookies=cookies, verify=False, headers = headers)
    data = json.loads(xml.text)
    return data

parse = argparse.ArgumentParser()

parse.add_argument('-d','--domain', help="Domain Url", required = True)
parse.add_argument('-f', '--FedAuth', help = 'Session Id Value', required = True)
parse.add_argument('-u', '--user', help = 'Find user information', required = False)
args = parse.parse_args()

headers = {
    "Accept": "application/json;odata=verbose"
}

cookies = {
    'FedAuth': args.FedAuth
    
    }


banner()
print('{} Obteniendo datos... {}'.format(fg('yellow'), attr('reset')))
try:
    data = miproperties()
    print('My Properties')
    printdata(data)
    if args.user is not None:
        print("Finding User....")
        usuario = urllib.quote(args.user)
        if not usuario.startswith('%27'):
            usuario = '%27' + usuario
        if not usuario.endswith('%27'):
            usuario = usuario + '%27' 

        data = finduser(usuario)
        printdata(data)
except requests.ConnectionError as ex:
    print('{} Error {}').format( fg('red'), ex.message , attr('reset'))
