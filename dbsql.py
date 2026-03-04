import pymssql
from dataclasses import dataclass
from datetime import datetime
                
@dataclass
class Sql_cnx:
   
   

   def __init__(self , server,user,password,database):
      self.server = server
      self.user = user
      self.password = password
      self.database = database
      self.cnx = None
       

   def set_cnx(self, cnx):
       self.cnx = cnx

   def get_cnx(self):
       return self.cnx
   
   def msql_close_cnx(self):
      if self.cnx:
        try:
            self.cnx.close()
            self.cnx = None
            print('Conexión a DB cerrada.')
        except pymssql.Error as e:
            # Es bueno loguear errores al cerrar para depuración
            print(f"Error al cerrar conexión a DB: {e}")
      else:
        print('No hay conexión a DB activa para cerrar.')

       
   #Conexion se ejecuta luego de init para crear conexion 
   def msql_conx(self):
      if self.cnx is None:
         try:
            conn = pymssql.connect(
            server = self.server,
            user = self.user,
            password = self.password,
            database = self.database,
            as_dict=True
          )
            self.set_cnx(conn)
       
         except pymssql.Error as e :
                  raise ConnectionError( f"Error iniciar sql cnx: {e} " )
      else:
        raise ConnectionError( 'Ya existe una conexión a DB activa.' )



   def msql_consulta( self  ):
      #busqueda en base de datos
      qr = """select  distinct master 
              , ( select mst_manifiesto  from masters_sunat_trazabilidad where mst_documento_transporte = master for json path ) as sunat  
            from masters 
            where  estado = 29 
                   and ((manif_nro='' or manif_nro is null) and ingreso_local is null) and negocio in (1)
                   or m_sunat_trazabilidad = 1
             order by 1 desc"""
      try:
        cur = self.get_cnx().cursor()
        cur.execute( qr )
        records = cur.fetchall()

        cur.close()
        return records
        
      except pymssql.Error as e :
        raise ConnectionError( f"Error consulta sql: {e} " )
    

   def msql_save_masters_sunat( self , d ):
      
      try:
        cur = self.get_cnx().cursor()
        #
        #
        qr = """INSERT INTO masters_sunat_trazabilidad ( 
                mst_manifiesto,   mst_fecha_llegada_estimada, 
                mst_vuelo,	mst_nave,
	              mst_fecha_llegada, 	mst_fecha_llegada_transmision ,
	              mst_fecha_termino_descarga , 	mst_linea_aerea ,
	              mst_indicador_carga , 	mst_estado_manifiesto ,
	              mst_documento_transporte , 	mst_puerto_inicio ,
	              mst_id_master , 	mst_nro_manifiesto  
                ) values(%s,%s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %d, %s  )"""
        
        qr1 = """UPDATE masters_sunat_trazabilidad  
             set mst_fecha_llegada = %s where mst_manifiesto = %s and mst_documento_transporte = %s """
        
        
        for v in d:
           if v[5] == '-': v[5] = ''  #si fecha de llegada es '-' comvertimos a ''
           #
           if v[15] == 0: #insert si no existe
              val = (  v[0], 
                    v[1], # para guardar date datetime.strptime(v[1], "%d/%m/%Y %H:%M:%S"), 
                    v[3], v[4], 
                    v[5], # datetime.strptime(v[5], "%d/%m/%Y %H:%M:%S"), 
                    v[6], # datetime.strptime(v[6], "%d/%m/%Y %H:%M:%S"), 
                    v[7], # datetime.strptime(v[7], "%d/%m/%Y %H:%M:%S"), 
                    v[8], v[9], v[10], v[11], 
                    v[12], v[13], v[14]   )
              cur.execute(qr, val )
              print('procesado '+v[11] )
              #
           elif v[15] == 1: #update fecha
              val1 = ( v[5], v[0] , v[11] )
              cur.execute(qr1, val1 )
              print('procesado up '+v[11] )
              #
           self.get_cnx().commit()
           #
           #
           #con toda la sunat ingresado luego por master vinculo tablas   
        for v1 in d:
          master = v1[11]
          #ejecucion de procedure
          if master :
             cur.callproc('proc_masters_sunat_trazabilidad', ( 1 , master+"" ))
             self.get_cnx().commit()
        #     
        cur.close()
      except pymssql.Error as e :
        raise ConnectionError( f"Error insert sql: {e} " )


