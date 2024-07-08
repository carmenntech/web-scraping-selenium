
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys #para enviar teclas  especiales
from config_insta_credenciales import *
from conexionbase_confi import *

import pickle #para cargar/guardar cookies
import time
import os
import pyodbc
import json



def iniciar_chrome():

    options = Options()
    #definir agente
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
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


def login_instagram():
    time.sleep(2)
    driver.get('https://www.youtube.com/')
    time.sleep(2)
    driver.execute_script("""                  
        var scrollt = document.querySelector('tp-yt-paper-dialog[id="dialog"]')
        scrollt.scrollTop = scrollt.scrollHeight
        """)
    

    #//button//span[contains(text(),'Aceptar todo')]
    permitir_cookies = driver.find_element(By.XPATH, ("//button[@class='yt-spec-button-shape-next yt-spec-button-shape-next--filled yt-spec-button-shape-next--mono yt-spec-button-shape-next--size-m']"))
    
    #damos al boton de cookies
    permitir_cookies.click()


def listar_videos():
    #print("paco paco paco " + driver)
    time.sleep(3)
    driver.get('https://www.youtube.com/@ClaudiaNicolasa/videos')
    time.sleep(5)



    for i in range(20):
        driver.execute_script("""
        var scrollt = document.querySelector('html')
        scrollt.scrollTop = scrollt.scrollHeight
        """)
        time.sleep(3)

        
    #cajita = driver.find_elements(By.XPATH, ("//div[@class='style-scope ytd-rich-grid-media' and @id='dismissible']"))

    videos_titulo_list = []
    videos_visualizaciones_list = []

    videos_titulo = driver.find_elements(By.XPATH, ("//div[@class='style-scope ytd-rich-grid-media']//yt-formatted-string[@id='video-title']"))
    videos_visualizaciones = driver.find_elements(By.XPATH, ("//span[@class='inline-metadata-item style-scope ytd-video-meta-block']"))

    #for caja in cajita:

    # Imprime el texto de cada seguidor
    for titulo in videos_titulo:
        
        videos_titulo_list.append(titulo.text)
    
    for visualizacion in videos_visualizaciones:
        
        videos_visualizaciones_list.append(visualizacion.text)

    datavideo_diccionario = {
        'lista1': videos_titulo_list,
        'lista3': videos_visualizaciones_list
    }

    # Convertir el diccionario a JSON
    json_data = json.dumps(datavideo_diccionario, indent=4)

    

    return     json_data 
                       
   



if __name__ == '__main__':

    driver = iniciar_chrome()

    login_instagram()

    wait = WebDriverWait(driver, 20)

    res = listar_videos()

    print(res)

    driver.quit()