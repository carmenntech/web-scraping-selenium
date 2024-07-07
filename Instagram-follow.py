
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys #para enviar teclas  especiales
from config_insta_credenciales import *
from conexionbase_confi import *

import pickle #para cargar/guardar cookies
import time
import os
import pyodbc

def iniciar_chrome():

    options = Options()
    #definir agente
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
    options.add_argument(f"user-agent={user_agent}")
    #definir las dimensiones de la ventana
    #options.add_argument("--window-size=1000,1000")
    #maximizar la ventana de chrome
    options.add_argument("--start-maximized")
    #ejecutar en segundo plano, sin mostrar
    #options.add_argument('--headless')
    #desactivar notificaciones
    options.add_argument('--disable-notifications')
    #desactivar flags de seguridad 
    options.add_argument('--disable-web-security')
    #desactiva sandbox aislar los procesos del navegador y evitar que los sitios web maliciosos ejecuten código en el equipo del usuario
    #options.add_argument('--no-sandbox')
    #options.add_argument("--disable-blink-features=AutomationCOntrolled")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    return driver

#### MAIN ####

def login_instagram():
    time.sleep(1.5)
    driver.get('https://www.instagram.com/')
    
    permitir_cookies = driver.find_element(By.XPATH, ("//button[contains(text(),'Permitir')]"))
    #damos al boton de cookies
    permitir_cookies.click()
    
    try:
        input_usuario = wait.until(ec.visibility_of_element_located((By.NAME, "username")))
    except TimeoutException as e:
        print('COmprobar usuario contraseña')
        return 'ERROR 0.1'
    
    #input_usuario = driver.find_element(By.NAME, ("username"))
    #para introducir el usuario 
    input_usuario.send_keys(USER_IG)
    input_pass = driver.find_element(By.NAME, ("password"))
    #para introducir la PSW 
    input_pass.send_keys(PASS_IG)

    b_iniciarsesion = wait.until(ec.element_to_be_clickable((By.CSS_SELECTOR, "button[type ='submit']")))
    b_iniciarsesion.click()

    b_guardarinfosesion = wait.until(ec.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Guardar información')]")))
    b_guardarinfosesion.click()

    #Comprobar que se ha cargado bien el feed
    try:
        comprobacioncarga = wait.until(ec.visibility_of_element_located((By.CSS_SELECTOR, "article[role ='presentacion']")))
        print('Log ok')
    except TimeoutException:
       print('Error el feed no se ha cargado')

    #para hacer scroll en la pagina


    #guardamos las cookies para hacer el inicio con las cookies
    #cookies = driver.get_cookie()
    #pickle.dump(cookies, open("instagram.cookies", "wb"))
    #return OK
       
def listar_seguidores(scrollseguidores):
    
    driver.get(f'https://www.instagram.com/{nombreusuario}/followers/')
    time.sleep(3)
    seguidores_usuario = set()

    i = 0
    
    # Encuentra el elemento específico para hacer scroll
    #scroll_elemento = driver.find_element(By.XPATH, "//div[@class='_aano']")
    #scroll_elemento = driver.find_element(By.CLASS_NAME, "_aano")

    while i <= scrollseguidores:
        driver.execute_script("""
        var scrollt = document.querySelector('div[class="_aano"]')
        scrollt.scrollTop = scrollt.scrollHeight
        """)
        time.sleep(1)  # Espera a que carguen más seguidores
        seguidos = driver.find_elements(By.XPATH, "//div[@class='_aano']//div[@class='x1rg5ohu']//span")
        # Encuentra todos los elementos de seguidores

        # Imprime el texto de cada seguidor
        for seguido in seguidos:
        
                seguidores_usuario.add(seguido.text)
  
        i+=1

    return seguidores_usuario                
   
def listar_seguidos(scrollseguidos):
    
    driver.get(f'https://www.instagram.com/{nombreusuario}/following/')
    time.sleep(3)

    seguidos_usuario = set()
    i=0
    # Haz scroll en el elemento para cargar más seguidores
    while i <= scrollseguidos:
        driver.execute_script("""
        var scrollt = document.querySelector('div[class="_aano"]')
        scrollt.scrollTop = scrollt.scrollHeight
        """)
        time.sleep(1)  # Espera a que carguen más seguidores
        seguidos = driver.find_elements(By.XPATH, "//div[@class='_aano']//div[@class='x1rg5ohu']//span")
        # Encuentra todos los elementos de seguidores

        # Imprime el texto de cada seguidor
        for seguido in seguidos:
        
                seguidos_usuario.add(seguido.text)
        
        i+=1

    return seguidos_usuario
       
def infosegui(nombreusuario, conexion):
    #///div[@class='_aano']//div[@class='x1rg5ohu']//span
    
    driver.get(f'https://www.instagram.com/{nombreusuario}/')
    time.sleep(1)
    numeroseguidores = driver.find_element(By.XPATH, (f"//a[@href='/{nombreusuario}/followers/']//span[@class='_ac2a']//span"))
    numeroseguidos = driver.find_element(By.XPATH, (f"//a[@href='/{nombreusuario}/following/']//span[@class='_ac2a']//span"))

    numeroseguidores_int = int(numeroseguidores.text)
    numeroseguidos_int = int(numeroseguidos.text)
    
    scrollseguidores = int(numeroseguidores.text) /12
    if scrollseguidores%2 == 0:
        scrollseguidores+=1
    scrollseguidores = int(scrollseguidores)

    scrollseguidos = int(numeroseguidos.text) /12
    if scrollseguidos%2 == 0:
        scrollseguidos+=1
    scrollseguidos = int(scrollseguidos)
    
    print(numeroseguidores.text, type(numeroseguidores.text))
    print(numeroseguidos.text, type(numeroseguidos.text))

    lista_seguidores = listar_seguidores(scrollseguidores)
    lista_seguidos = listar_seguidos(scrollseguidos)
    
    print(f"Seguidores listados: {len(lista_seguidores)}")
    print(f"Seguidos listados: {len(lista_seguidos)} ")

    try:
        print(f"Diferencia Seguidores: {((numeroseguidores_int) - (len(lista_seguidores)))}")
        print(f"Diferencia Seguidos: {((numeroseguidos_int) - (len(lista_seguidos)))}")

    except Exception as e:
    # Manejo de la excepción
        print("Se produjo una excepción:", e)

    #print("**********")
    #print(lista_seguidores)
    #print(lista_seguidos)

    conexion.ejecutar_consulta("INSERT INTO idnombre_usuariosig (nombre_usuarioig) VALUES (?)", nombreusuario)
    conexion.commit()

    # Insertar los valores en la tabla Seguidos
    for seguidor in lista_seguidores:
        conexion.ejecutar_consulta("INSERT INTO idnombre_usuariosig (nombre_usuarioig) VALUES (?)", seguidor)
        conexion.commit()
    
    for seguidor in lista_seguidores:
        
        conexion.ejecutar_consulta("""
            INSERT INTO seguidos_usuariosig (id_seguidor, id_user)
            SELECT id_usuarioig, (SELECT  [id_usuarioig] FROM [PRUEBAS].[dbo].[idnombre_usuariosig] where nombre_usuarioig = ? )
            FROM [idnombre_usuariosig]
            WHERE nombre_usuarioig = ?;
        """
        , (nombreusuario, seguidor))
        conexion.commit()


    for seguidos in lista_seguidos:
        conexion.ejecutar_consulta("INSERT INTO idnombre_usuariosig (nombre_usuarioig) VALUES (?)", seguidos)
        conexion.commit()

    for seguidos in lista_seguidos:
        
        conexion.ejecutar_consulta("""
            INSERT INTO seguidos_usuariosig (id_seguidor, id_user)
            SELECT (SELECT  [id_usuarioig] FROM [PRUEBAS].[dbo].[idnombre_usuariosig] where nombre_usuarioig = ? ), id_usuarioig 
            FROM [idnombre_usuariosig]
            WHERE nombre_usuarioig = ?;
        """
        , (nombreusuario, seguidos))
        conexion.commit()


    time.sleep(1)

    for seguido in lista_seguidos:

        if seguido not in lista_seguidores:

            print(seguido)



    
    



if __name__ == '__main__':
    nombreusuario = input("Escribe el usuario que desas analizar: ")

    conexion = ConexionBBDD(servidor='localhost', base_datos='PRUEBAS', usuario='sa', contrasena='12345', driver = '{ODBC Driver 17 for SQL Server}' )

    conexion.conectar()

    driver = iniciar_chrome()

    wait = WebDriverWait(driver, 15)

    res = login_instagram()

    infosegui(nombreusuario, conexion)

    if res == 'ERROR 0.1':
        print('Comprobar usuario contraseña')

    conexion.cerrar_conexion()
    
    driver.quit()
    
    
