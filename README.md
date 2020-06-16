# SharePointTools

### Herramientas en Python que permiten el descubrimiento y analisis de recuroso de SharePoint 


# sharepointdiscoverlists.py
Script de Python 2.7, el cual permite descrubir todas aquellas paginas de administracin que se encuentran sin autenticacion.

<b>Actualmente no Soporta SSL </b>

Uso

![alt text](https://raw.githubusercontent.com/daniel2005d/SharePointTools/master/usosharepoindiscover.png  "Ayuda")



###### python sharepointdiscoverlists.py -h 



```python

-d --dominio direccion url del sitio a escanear (Obligatorio)
-f --file Direccion de Direccion de las listas, en caso de no especificar, se tomaran las que se establecen por defecto.
-s --sitemap Direccion Url donde se encuentra el sitemap```

## getusers.py
Script en python que permite obtener todos los usuarios del sitio

```python
-d --domain Dirección del sitio web
-c --cookie, cookies que se requieren para realizar la petición. Cada una debe ir especificada a parte. Ejemplo: -c "Cookie1:Valor" -c "Cookie2:Valor2"

 