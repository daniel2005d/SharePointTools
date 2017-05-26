#!/usr/bin/env python
import os
import urllib2
from colored import fg, attr
import argparse
import sys
import socket
from bs4 import BeautifulSoup as bs


#*******************************
#Definicion de Clase
#*******************************


class SharePointScanner:
    """Constructor de la Clase"""
    def __init__(self, host, archivo, usarsitemap):

        self.adminpages = ['_layouts/viewlsts.aspx', '_layouts/authenticate.aspx', '_layouts/settings.aspx', 'catalogs/lt']
        self.host = host
        self.archivo = archivo
        self.usarsitemap = usarsitemap

    def log(self, mensaje, tipo):
        color = tipo
        if tipo == 1:
            color = 9
        elif tipo == 2:
            color = 10
        elif tipo == 3:
            color = 11

        print ('%s %s %s' % (fg(color), mensaje, attr('reset')))

    """Se encarga de obtener el XML y asi devolver el arreglo de paginas"""
    def leersitemap(self):
        def payload(sitemapurls):
            paginas = []
            for d in sitemapurls:
                parts = d.split('/')
                url = d.replace(parts[len(parts) - 1], '')
                for a in self.adminpages:
                    paginas.append(url + a)
            return paginas

        """Carga todos los dominios a partir del XML
        y devuelve una arreglo con los dominios encontrados"""
        def crearurls():
            urls = []
            try:
                """Transforma el XML del Sitemap"""
                sitemap = urllib2.urlopen(self.usarsitemap)
                soup = bs(sitemap.read(), 'html.parser')
                loc = soup.find_all('loc')
                for l in loc:
                    urls.append(l.get_text())
                return urls
            except NameError as n:
                self.log(n, 1)
            except:
                self.log(('Ocurrio un error al leer el sitemap %s' % sys.exc_info()[0]), 1)
        """Arma las Uri de acuerdo al sitemap establecido"""
        sitemap = crearurls()
        return payload(sitemap)

    """Lee el archivo que se establecio en el atributo
    el cual contiene las paginas de Administracion de SharePoint"""
    def cargarArchivo(self):
        if self.archivo is not None:
            self.log('==================', 2)
            self.log('Leyendo el Archivo', 2)
            self.log('==================', 2)
            lines = open(self.archivo, 'r').readlines()
            for l in lines:
                page = l.replace('\n', '')
                if page not in self.adminpages:
                    self.adminpages.append(page)

    """Carga los datos de acuerdo a los establecido en los parametros"""
    def parcear(self):
        self.cargarArchivo()
        if (self.usarsitemap is not None):
            treepages = self.leersitemap()
            for t in treepages:
                self.adminpages.append(t)

    """Realiza el scaneo del sitio"""
    def iniciar(self):
        exitosos = []
        """Carga los objetos acorde a lo establecido en los parametros"""
        self.parcear()
        self.log('==============================', 2)
        self.log('Iniciando Proceso de Scaneo', 2)
        self.log('=============================', 2)

        for l in self.adminpages:
            if l.startswith('http'):
                urllista = l
            else:
                urllista = self.host + l
            try:
                response = urllib2.urlopen(urllista)
                codigo = response.getcode()
                self.log(('%s -- [%i]' % (urllista, codigo)), 83)
                if codigo == 200:
                    exitosos.append(urllista)

            except urllib2.HTTPError as e:
                self.log(('%s -- [%i:%s]' % (urllista, e.code, e.reason)), 116)
            except urllib2.URLError as u:
                print '%s %s %s %s [%s] %s' % (fg(11), urllista, attr('reset'), fg(1), u.reason, attr('reset'))
            except socket.error as s:
                print s
            except KeyboardInterrupt:
                print '%s Proceso cancelado %s' % (fg(1), attr('reset'))
                return exitosos
            except TypeError as t:
                print '%s %s [%s] %s' % (fg(1), urllista, t, attr('reset'))
            except:
                self.log(('%s [%s]' % (urllista, sys.exc_info()[0])), 190)
        return exitosos

parser = argparse.ArgumentParser(description='Descubre las URLs de SharePoint' +
'que estan sin autenticacion')
parser.add_argument('-d', '--dominio', help='Url del dominio')
parser.add_argument('-f', '--file', help='Archivo con las URLs de ' +
'administracion de Sharepoint. En caso de no especificar se tomaran las que ' +
'se establecen por defecto.')
parser.add_argument('-s', '--sitemap', help='Direccion URL donde se encuentra el sitemap, con el fin de poder usarlo para armar las URLs')
parser.add_argument('-v', '--version', help='Muestra la version actual', action='store_true')
args = parser.parse_args()
dominio = ''
version = 'Version 1.3'


if args.version:
    print '%s %s %s' % (fg(11), version, attr('reset'))
    exit(0)

if args.dominio is None:
    parser.print_help()
    exit(0)
elif args.dominio.endswith('/'):
    dominio = args.dominio
else:
    dominio = args.dominio + '/'

os.system('clear')

print ("""
   _____ _____    _____  _
  / ____|  __ \  |  __ \(_)
 | (___ | |__) | | |  | |_ ___  ___ _____   _____ _ __
  \___ \|  ___/  | |  | | / __|/ __/ _ \ \ / / _ \ '__|
  ____) | |      | |__| | \__ \ (_| (_) \ V /  __/ |
 |_____/|_|      |_____/|_|___/\___\___/ \_/ \___|_|


""")
sp = SharePointScanner(dominio, args. file, args.sitemap)
exitosos = sp.iniciar()
sp.log('Resumen de la Ejecucion', 3)
sp.log('================', 231)
for e in exitosos:
    sp.log(e, 200)
sp.log('================', 231)