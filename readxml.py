import sys
import xml.etree.ElementTree as ET
import urllib2

def leersitemap():
   response = urllib2.urlopen('http://www.avianca.com/es-co/sitemap.xml')
   f = open('sitemap.xml','w')
   if (response.getcode() == 200):
       sitemap = response.read()
       f.write(sitemap)
       return sitemap
       
      
   
def crearurls(xml):
    urls = []
    #tree = ET.fromstring(xml)
    tree = ET.parse('sitemap.xml')
	#root = tree.findall('{http://www.sitemaps.org/schemas/sitemap/0.9}url')
    root = tree.getroot()
    for child in root:
        c = child.findall('{http://www.sitemaps.org/schemas/sitemap/0.9}loc')
        for x in c:
            urls.append(x.text.replace('\n',''))

    return urls

def payload(direcciones):
    for d in direcciones:
	   parts = d.split('/')
	   segments = ' '.join(parts).split()
	   print "====================="
	   for p in segments:
	      
   
xml = leersitemap()
direcciones = crearurls(xml)
payload(direcciones)