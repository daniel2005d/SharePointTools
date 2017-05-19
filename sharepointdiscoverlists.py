import os
import urllib2
from colored import fg, attr
#from numpy import array
import argparse
import sys
import socket

parser = argparse.ArgumentParser(description='Descubre las URLs de SharePoint' +
'que estan sin autenticacion')
parser.add_argument('-d', '--dominio', help='Url del dominio')
parser.add_argument('-f', '--file', help='Archivo con las URLs de ' +
'administracion de Sharepoint. En caso de no especificar se tomaran las que ' +
'se establecen por defecto.')
args = parser.parse_args()
dominio = ''
os.system('clear')

listas = ['_layouts/viewlsts.aspx','_layouts/authenticate.aspx','_layouts/settings.aspx','_catalogs/lt']
adminlists = []

def scanear():
   print '%s Inicia Scaneo SharePoint \n %s' % (fg('104'),attr('reset'))
   global dominio
   for l in adminlists:
     urllista = dominio + l
     try:
       codigo = urllib2.urlopen(urllista).getcode()
       print '%s %s [$i] %s' % (fg(107),urllista,codigo,attr('reset'))
     except urllib2.HTTPError as e:
       print '%s %s %s %s [%i:%s] %s' % (fg(11),urllista,attr('reset'),fg(1), e.code,e.reason, attr('reset'))
     except urllib2.URLError as u:
         print '%s %s %s %s [%s] %s' % (fg(11),urllista,attr('reset'),fg(1), u.reason, attr('reset'))
     except socket.error as s:
       print s
     except KeyboardInterrupt:
       print '%s Proceso cancelado %s' % (fg(1),attr('reset'))
       exit(0)
     except TypeError as t:
       print '%s %s [%s] %s' % (fg(1), urllista, t, attr('reset'))
     except:
       print '%s %s [%s] %s' % (fg(1),urllista,sys.exc_info()[0],attr('reset'))

if args.dominio is None:
  parser.print_help()
else:
  if args.dominio.endswith('/'):
     dominio = args.dominio
  else:
    dominio = args.dominio + '/'

if args.file is None:
  adminlists = listas
else:
  direcciones = open(args.file, 'r').readlines()
  for l in direcciones:
     adminlists.append(l.replace('\n',''))

#print adminlists
scanear()
