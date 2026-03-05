from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
from selenium.common.exceptions import NoAlertPresentException, UnexpectedAlertPresentException

import io

def www_sunat_manifiesto( dr , **kwargs ):
    
    
#para ver la pagina

    try:
        ele = WebDriverWait(dr,20).until( EC.presence_of_element_located((By.NAME,'CMc1_Numero'))   ) 
        
        anho = dr.find_element(By.NAME, 'CMc1_Anno')
        anho.clear()
        anho.send_keys( kwargs["anho"] )  #año 

        manif = dr.find_element(By.NAME, 'CMc1_Numero')
        manif.clear()
        manif.send_keys( kwargs["manif"] )  #nro manif

        bt = dr.find_element(By.XPATH, "//input[@type='BUTTON']")
        bt.click()

        su = BeautifulSoup(dr.page_source, 'html.parser')
        a = su.find_all( 'table' )
        c = a[2].find_all( 'td' )

    #Manifiesto
        r = {}

        r["manif"] = c[1].get_text().strip()
        r["f_llegada"] = c[5].get_text().strip()
        r["aereolinea"] = c[9].get_text().strip()

        return r
        

        

    except:
        print( 'Error Scraping' )
        




def www_sunat_login( dr , **kwargs ):
    try:
        ele = WebDriverWait(dr,15).until( EC.presence_of_element_located(( By.XPATH, "//a[@href='javascript:tramiteConsulta()']" ))   )
        original_window = dr.current_window_handle

        li = dr.find_element( By.XPATH, "//a[@href='javascript:tramiteConsulta()']" )
        li.click()
        
        dr.switch_to.window( dr.window_handles[1]  ) #para saltar a pagina flotante

        ele = WebDriverWait(dr,15).until( EC.presence_of_element_located(( By.ID , 'txtRuc' ))   )
        dr.implicitly_wait(10)

        # LOGIN SUNAT
        ruc = dr.find_element(By.ID , 'txtRuc' )
        ruc.clear()
        ruc.send_keys( kwargs["txtRuc"] )

        user = dr.find_element(By.ID , 'txtUsuario' )
        user.clear()
        user.send_keys( kwargs["txtUsuario"] )  

        pas = dr.find_element(By.ID , 'txtContrasena' )
        pas.clear()
        pas.send_keys( kwargs["txtContrasena"] )

        bt = dr.find_element(By.ID , "btnAceptar" )
        bt.click()    
        
        # ele = WebDriverWait(dr,20).until( EC.presence_of_element_located(( By.XPATH, "//li[@id='nivel2_28_1']" ))   )
        dr.implicitly_wait(7)

    except Exception as ex:
        raise TimeoutError( f"Error sunat login {ex}" )


def www_sunat_traza_link( dr ):
    try:
        
        menu = WebDriverWait(dr, 15).until( EC.element_to_be_clickable((By.XPATH, "//div[@id='divOpcionServicio3']"))   )
        dr.execute_script("arguments[0].scrollIntoView({block: 'center'});", menu)
        dr.execute_script("arguments[0].click();", menu)
        
        menu1 = WebDriverWait(dr, 15).until( EC.element_to_be_clickable((By.XPATH, "//li[@id='nivel2_28_1']"))   )
        dr.execute_script("arguments[0].scrollIntoView({block: 'center'});", menu1)
        dr.execute_script("arguments[0].click();", menu1)

        menu2 = WebDriverWait(dr, 15).until( EC.element_to_be_clickable((By.XPATH, "//li[@id='nivel3_28_1_2']"))   )
        dr.execute_script("arguments[0].scrollIntoView({block: 'center'});", menu2)
        dr.execute_script("arguments[0].click();", menu2)

        menu3 = WebDriverWait(dr, 10).until( EC.element_to_be_clickable((By.XPATH, "//li[@id='nivel4_28_1_2_1_1']"))   )
        dr.execute_script("arguments[0].scrollIntoView({block: 'center'});", menu3)
        dr.execute_script("arguments[0].click();", menu3)

        
    except Exception as ex:
        raise TimeoutError( f"Error sunat traza ingreso {ex}" )

   
    

def www_sunat_traza_manifiesto( dr , **kwargs ):

    try:
        
        
        WebDriverWait(dr,3).until( EC.presence_of_element_located(( By.NAME , 'codigoAduana' ))   ) 
        s = Select( dr.find_element(By.NAME , 'codigoAduana' )) #select como aereo
        s.select_by_index( 2 )
        
        
        WebDriverWait(dr,3).until( EC.presence_of_element_located(( By.NAME , 'viaTransporte' ))   )
        s = Select( dr.find_element(By.NAME , 'viaTransporte' )) #select como aereo
        s.select_by_index( 1 )
       

        WebDriverWait(dr,3).until( EC.presence_of_element_located(( By.NAME ,  'selLugarIngreso'  ))   )
        s = Select( dr.find_element(By.NAME , 'selLugarIngreso' )) #select como aereo
        s.select_by_index( 1 )
        

        WebDriverWait(dr,3).until( EC.presence_of_element_located(( By.ID, "rbNumeroDocuDeTransporte"  ))   )
        e = dr.find_element( By.ID, "rbNumeroDocuDeTransporte"  ) 
        e.click()

        e = dr.find_element(By.ID , 'txtNumeroDocTransporte' )
        e.clear()
        e.send_keys( kwargs["master"] ) #busqueda por master
     
        e = dr.find_element(By.ID , 'btnConsultar' )
        e.click()
        dr.implicitly_wait(5)
    
        #cuando se tiene resultado de la busqueda
        try:
            WebDriverWait(dr,10).until( EC.presence_of_element_located(( By.XPATH, "//table[@id='tblManifiestoCarga']" ))   )
            su = BeautifulSoup(dr.page_source, 'html.parser')
            a = su.find( 'table' , id="tblManifiestoCarga" )
            c = a.find_all( 'td' )
            
            d = []
            d.clear()
            for v in c:
              d.append( v.get_text().strip() )
        
            
            dr.switch_to.default_content()
            x = dr.find_element( By.XPATH, "//li[@id='nivel4_28_1_2_1_1']"  ) #consultas trazabilidda
            dr.execute_script("arguments[0].click();", x )
            dr.switch_to.frame("iframeApplication")
            print("paso 4")
            return d

        #cuando no se tiene resultado de la busqueda, no se muestra la tabla y se muestra error 
        except:
            su = BeautifulSoup(dr.page_source, 'html.parser')
            e = su.find( 'div' , id="divMsjErrorDatosGenerales" )
            print( kwargs["master"] )
            return e.get_text().strip() 
            


    except UnexpectedAlertPresentException as e:
        print('alert sesion expirada')
        alert = dr.switch_to.alert
        alert.accept()
        raise ConnectionError( f"Error se inicio ALERT {e}" )
        
    except Exception as ex:
        #verificacion de algun aler
        print( "Exceptio inicio" )
        try:
           alert = dr.switch_to.alert
           print(f"Texto de la alerta: {alert.text}")
           alert.accept()  # Acepta la alerta (hace clic en OK)
        except NoAlertPresentException:
           print("No se encontró ninguna alerta de JavaScript.")
         
        raise TimeoutError( f"Error sunat de scraping manifiesto {ex}" )
        