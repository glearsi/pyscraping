from selenium import webdriver
from scair import www_sunat_traza_manifiesto , www_sunat_login , www_sunat_traza_link 
from dbsql import Sql_cnx
import numpy
import json 



class Sunat_aereo:

      
   def __init__(self):
      #URL to scraping
      self.url = 'xxURLxx'
       
   
   

   def busqueda_sunat(self):
      dr = None
      c = None
      try:
         #Inicio conexion con WEB
         dr = webdriver.Firefox()
         dr.get(self.url) 
         www_sunat_login( dr, txtRuc='xxRUCxx' , txtUsuario='xxUSUARIOxx' , txtContrasena='xxCONTRASENAxx' )
         www_sunat_traza_link(dr)
         #ubicamos en el iframe
         dr.switch_to.frame("iframeApplication")
         
         #creo conexion DB
         c = Sql_cnx( 'xxIP/INSTANCIAxx', 'xxUSUARIOxx', 'xxPASSWORDxx', 'xxDBxx' )
         c.msql_conx() #creo conexion
      
         r0 = c.msql_consulta() #almacena resultado de la busqueda en DB 
         l0 = [] # init arreglo para las busquedas
         se_manifiesto = lambda x, i: x[ len(x)-i ]
     
         #recorro resultado de la busqueda en DB
         for f0 in r0:
            #envio resultado de la pagina web y el dato a ser buscado a scraping
            d = www_sunat_traza_manifiesto( dr , master=f0['master'] )
            if isinstance( d, list):
               p = len(d)/13 #cantidad de filas
               if p > 1: # si tengo mas de un fila
                  l = numpy.array_split( d , p) # divido segun cantidad de valores
                  for f1 in l:
                     de = dict(enumerate(f1)) #cada lista la combierto en dict 
                     de[13] = 0 # ID DEL MASTER
                     de[14] = int( se_manifiesto( de[0].split('-'), 1 ) ) 
                     #nuevo
                     if f0['sunat'] is None:  
                        de[15] = 0
                     #
                     #update fecha o es uno nuevo
                     else:
                        dver = json.loads(f0['sunat']) #cargo como dict respuesta json de SQL 
                        if any( res["mst_manifiesto"] == de[0] for res in dver ) : #busca en todas las lista  si existe el valor
                           de[15] = 1
                        else: 
                           de[15] = 0
                     #
                     if len(de) == 16: l0.append(de)
                     #            
               else: #para solo una fila
                  de = dict(enumerate(d))
                  de[13] = 0 #f0['id_master']
                  de[14] = int( se_manifiesto( de[0].split('-'),1 )  )
                  #
                  #nuevo
                  if f0['sunat'] is None:  de[15] = 0
                  #update fecha si existe registro
                  else: de[15] = 1
                  #
                  if len(de) == 16: l0.append(de)
            else:
               #mensaje cuando no tiene manifiestos
               print( d )
               # 
               # 
               #   
         if len(l0) >0 : c.msql_save_masters_sunat( l0 ) #guarda en base de datos toda la lista
         c.msql_close_cnx()  #cerrar conexcion
         dr.quit() #cierro driver
         #
      except (TimeoutError, ConnectionError) as e:
         if c is not None: c.msql_close_cnx()  #cerrar conexion
         if dr is not None: dr.quit() #cierro driver
         print( f"Error excepcion: {e}" )
      finally:
         if c is not None: c.msql_close_cnx()  #cerrar conexion
         if dr is not None: dr.quit() #cierro driver
         print( f"Finalizacion " ) 
            





