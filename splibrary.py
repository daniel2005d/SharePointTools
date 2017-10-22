#!/usr/bin/env python
from colored import fg, attr
import argparse
from bs4 import BeautifulSoup 
from urlparse import urlparse
import requests
import sys

def validaracceso(pagina):
    r = requests.get(pagina, verify=False)
    if r.status_code == 200:
        print('{} {} {} --> {} OK {}'.format(fg('yellow'), pagina, attr('reset'), fg('green'), attr('reset')))
    else:
        print('{} {} {} --> {} Error {} {}'.format(fg('red'), pagina, attr('reset'), fg('green'), r.status_code, attr('reset')))

    return r.status_code
def obtenerListas(sitio):
    paginas = []
    segmentosdominio = urlparse(sitio)
    dominio = segmentosdominio.scheme + '://' + segmentosdominio.netloc + '/'
    l = requests.get(sitio, verify=False)
    if (l.status_code == 200):
        soup = BeautifulSoup(l.text, 'html.parser')
        divs = soup.findAll('div',{"class":"ms-vl-apptile"})
        #hijos = divs.findChildren()
        for link in divs:
            vinculos = link.find_all('a')
            for href in vinculos:
                urllista = href.attrs['href']
                if urllista != 'javascript:;':
                    if urllista not in paginas:
                        codigo = validaracceso(dominio + urllista)
                        paginas.append({'pagina':urllista, 'status':codigo})
                        
    return paginas

parser = argparse.ArgumentParser(description='Obtiene los vinculos accesibles de las bibliotecas y listas de SharePoint')
parser.add_argument('-p','--pagina', help='Direccion de la pagina donde se encuentra el listado de Bibliotecas (viewlsts.aspx)', required=True)
parser.add_argument('-o','--output', help='Archivo de Salida de las Urls encontradas', required=False)
args = parser.parse_args()
if args.pagina is not None:
    print('%s Iniciando el descubrimiento %s' % (fg('green'), attr('reset')))
    try:
        paginas = obtenerListas(args.pagina)
        if args.output is not None:
            f = open(args.output,'w')
            for p in paginas:
                f.write(p['pagina'] + '-->' + str(p['status']) + '\n')

    except:
        print sys.exc_info()[0]