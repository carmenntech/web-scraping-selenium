from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup


options = Options()
options.add_argument("--no-sandbox")
options.add_argument("--headless")
options.add_argument("--disable-dev-shm-usage")
#ser = Service("C:\\Users\\Carmen\\AppData\\Local\\Programs\\Python\\Python312\\chromedriver.exe")
driver = driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
# Especificar la ruta personalizada del ChromeDriver
url = 'https://www.youtube.com/@ClaudiaNicolasa/videos'
driver.get(url)

print(driver.title)
#print(driver.page_source)

soup = BeautifulSoup(driver.page_source, 'html.parser')

print(soup.find(class_="style-scope ytd-c4-tabbed-header-renderer"))