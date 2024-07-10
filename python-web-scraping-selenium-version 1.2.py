
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
import pandas as pd




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
    time.sleep(3)
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
    driver.get('https://www.youtube.com/@amaiaromero/videos')
    time.sleep(5)



    for i in range(8):
        driver.execute_script("""
        var scrollt = document.querySelector('html')
        scrollt.scrollTop = scrollt.scrollHeight
        """)
        time.sleep(3)

        
    #cajita = driver.find_elements(By.XPATH, ("//div[@class='style-scope ytd-rich-grid-media' and @id='dismissible']"))

    videos_titulo_list = []
    videos_visualizacionesyfecha_list = []
    videos_visualizacionessolo_list = []
    videos_fechasolo_list = []
    videos_user_list = []

    videos_titulo = driver.find_elements(By.XPATH, ("//div[@class='style-scope ytd-rich-grid-media']//yt-formatted-string[@id='video-title']"))
    videos_visualizaciones = driver.find_elements(By.XPATH, ("//span[@class='inline-metadata-item style-scope ytd-video-meta-block']"))
    videos_nombreuser = driver.find_element(By.XPATH, ("//span[@class='yt-core-attributed-string yt-content-metadata-view-model-wiz__metadata-text yt-core-attributed-string--white-space-pre-wrap yt-core-attributed-string--link-inherit-color']"))

    #for caja in cajita:

    # Imprime el texto de cada seguidor
    for titulo in videos_titulo:
        
        videos_titulo_list.append(titulo.text)
    
    for visualizacion in videos_visualizaciones:
        
        videos_visualizacionesyfecha_list.append(visualizacion.text)
    

    for indice, valor in enumerate(videos_visualizacionesyfecha_list):
        if indice % 2 == 0:
            videos_visualizacionessolo_list.append(valor)
        else:
            videos_fechasolo_list.append(valor)

    datavideo_diccionario = {
        'titulo': videos_titulo_list,
        'views': videos_visualizacionessolo_list,
        'fecha': videos_fechasolo_list,
        'user': videos_nombreuser.text
    }

    # Convertir el diccionario a JSON
    json_data = json.dumps(datavideo_diccionario, indent=4)
    data = json.loads(json_data)
    df = pd.DataFrame(data)
    
    # Definir la ruta donde se guardará el archivo JSON
    file_path = r'C:/Users/Carmen/Desktop/py/videos.json'
    file_path_csv = r'C:/Users/Carmen/Desktop/py/videos.csv'
    dir_path = os.path.dirname(file_path)


    # Guardar el objeto JSON en el archivo con manejo de errores
    try:
        with open(file_path, 'w', encoding='utf-8') as json_file:
            json.dump(datavideo_diccionario, json_file, ensure_ascii=False, indent=4)
        print(f"Archivo JSON guardado en: {file_path}")
    except Exception as e:
        print(f"Ocurrió un error al guardar el archivo JSON: {e}")

    # Guardar el DataFrame en un archivo CSV con codificación UTF-8
    try:
        df.to_csv(file_path_csv, index=False, encoding='utf-8')
        print(f"Archivo CSV guardado en: {file_path_csv}")
    except Exception as e:
        print(f"Ocurrió un error al guardar el archivo CSV: {e}")

    return json_data


    print(df)
    return json_data 
                       
   



if __name__ == '__main__':

    driver = iniciar_chrome()

    login_instagram()

    wait = WebDriverWait(driver, 20)

    res = listar_videos()

    print(res)

    driver.quit()