import sys
import xml.etree.ElementTree as ET
import urllib2

pageadmin = ['/_layouts/settings.aspx','/_layouts/viewlsts.aspx']

def leersitemap():
   proxy = urllib2.ProxyHandler({'http': 'porvenirafp\por02408:Porvenir*69655@172.17.10.3:8080'})
   opener = urllib2.build_opener(proxy)
   urllib2.install_opener(opener)
   response = urllib2.urlopen('https://www.colmedica.com/sitemap.xml')
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
    global pageadmin
    paginas = []
    for d in direcciones:
       parts = d.split('/')
       segments = ' '.join(parts).split()
       url = ''
       for p in range(len(segments)):
           
           if p<len(segments)-1:
             if p == 0:
                url = url+ segments[p]+'/'
             else:
                url = url +'/' + segments[p]
       for a in pageadmin:
            paginas.append(url+a)
    return paginas
   
xml = leersitemap()
direcciones = crearurls(xml)
paginas = payload(direcciones)
for p in paginas:
   response = urllib2.urlopen(p)
   print response.getcode(),p