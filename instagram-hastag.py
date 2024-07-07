
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
import pickle #para cargar/guardar cookies
import time

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
    #try:
    #    comprobacioncarga = wait.until(ec.visibility_of_element_located((By.CSS_SELECTOR, "article[role ='presentacion']")))
    #    print('Log ok')
    #except TimeoutException:
    #   print('Error el feed no se ha cargado')

    #para hacer scroll en la pagina

def scroll_paginaprincipal():
    
    driver.get('https://www.instagram.com/')
    
    """
    scroll =  driver.find_element(By.CSS_SELECTOR, "html")
    for n in range(4):
        scroll.send_keys(Keys.PAGE_DOWN)
    """
    #usar javascrip con python
    for n in range(4):
        #scroll con javascrip
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        time.sleep(1)


    #guardamos las cookies para hacer el inicio con las cookies
    #cookies = driver.get_cookie()
    #pickle.dump(cookies, open("instagram.cookies", "wb"))
    #return OK

if __name__ == '__main__':
    driver = iniciar_chrome()

    wait = WebDriverWait(driver, 10)

    res = login_instagram()

    if res == 'ERROR 0.1':
        print('Comprobar usuario contraseña')

    #time.sleep(1)
    res = scroll_paginaprincipal()

    input('Pulsa enter para salir')
    driver.quit()
    
