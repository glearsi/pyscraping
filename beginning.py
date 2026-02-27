import time
import schedule
from sunat_trazabilidad import Sunat_aereo
from datetime import datetime

def task_sunat_trazabilidad():
    try:
        fecha_actual1 = datetime.now()
        fecha_formateada1 = fecha_actual1.strftime("%Y-%m-%d %H:%M:%S") #formateo y paso a texto
        print('Start '+fecha_formateada1 )
        
        a = Sunat_aereo()
        a.busqueda_sunat()
        
        fecha_actual = datetime.now()
        fecha_formateada = fecha_actual.strftime("%Y-%m-%d %H:%M:%S") #formateo y paso a texto
        print('Processed '+fecha_formateada )
    
    except Exception as e:
        print( f"Errorx: {e}")


if __name__ == "__main__":
    schedule.every(2).minutes.do( task_sunat_trazabilidad )
    while True:
        schedule.run_pending()
        time.sleep(5)