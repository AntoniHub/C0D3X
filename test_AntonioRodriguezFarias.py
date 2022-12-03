from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time


#Inicializamos el 'chromedriver.exe'
path = Service('Driver/chromedriver.exe')
driver = webdriver.Chrome(service=path)


#Abrimos la pagina principal de MercadoLibre
def test_abrirML():
    driver.get('https://mercadolibre.com/')
    driver.maximize_window()
    time.sleep(1)

#################################### SPAM ####################################
    driver.execute_script('alert("!!! GRACIAS por ver mi codigo !!!")')     ##
    time.sleep(1.5)                                                         ##
    ActionChains(driver).key_down(Keys.TAB).key_up(Keys.TAB).perform()      ##
    ActionChains(driver).key_down(Keys.TAB).key_up(Keys.TAB).perform()      ##
    time.sleep(1)                                                           ##
    ActionChains(driver).key_down(Keys.ENTER).key_up(Keys.ENTER).perform()  ##
    time.sleep(0.8)                                                         ##
#################################### SPAM ####################################

#Seleccionamos pais (Argentina)
def test_seleccionarArg():
    arg = driver.find_element(By.XPATH,'//a[@id="AR"]')
    arg.click()
    time.sleep(0.8)

#Aceptamos cookies
def test_aceptCookie():
    cookie = driver.find_element(By.XPATH,'//button[contains(text(),"Entendido")]')
    cookie.click()
    time.sleep(1)

#Abrimos la seccion de CATEGORIAS
def test_comboCategories():
    categorie = driver.find_element(By.XPATH,'/html/body/header/div/div[2]/ul/li[2]/a')
    categorie.click()
    time.sleep(0.5)

#Seleccionamos SUB-SECCION de TECNOLOGIA
def test_selectTecnologia():
    tecnologia = driver.find_element(By.CLASS_NAME,'nav-categs-departments__list--dynamic')
    tecnologia.click()
    time.sleep(0.5)

#Seleccionamos el apartado de PC
def test_openPC():
    pc = driver.find_element(By.XPATH,'/html/body/header/div/div[2]/ul/li[2]/div/div/div/div/div[2]/ul/li[4]/a')
    pc.click()
    time.sleep(0.8)

#Cancelamos anuncio de ubicacion
def test_cancelAlert():
    alerta = driver.find_element(By.CLASS_NAME,'andes-tooltip-button-close')
    alerta.click()
    time.sleep(0.8)

#Seleccionamos y Destildamos FILTRO por 'LLEGA MANANA'
def test_llegaManana():
    manana1 = driver.find_element(By.CLASS_NAME,'andes-checkbox__mimic')
    manana1.click()
    time.sleep(1.2)   #Para que cargue el filtro
    manana2 = driver.find_element(By.CLASS_NAME,'ui-search-filter-highlighted__switch-container')
    manana2.click()  #Reestablecer valores
    time.sleep(1.2) #Para que cargue el filtro

#Seleccionamos filtro 'MAS RELEVANTES'
def test_masRelevantes():
    relevantes = driver.find_element(By.CLASS_NAME,'andes-dropdown__standalone-arrow')
    relevantes.click()
    time.sleep(0.8)

#Seleccionamos por 'MENOR PRECIO'
def test_menorPrecio():
    menorPrecio = driver.find_element(By.XPATH,'//*[@id="root-app"]/div/div[1]/section/div[1]/div/div/div/div[2]/div/div/div/ul/a[1]')
    menorPrecio.click()
    time.sleep(0.8)

#Scrolleamos hasta el final de la pagina
def test_scrollDown():
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1.5)

#Pulsamos en 'SIGUIENTE PAGINA'
def test_nextPage():
    next = driver.find_element(By.XPATH,'//*[@id="root-app"]/div/div[1]/section/div[3]/ul/li[3]/a/span[1]')
    next.click()
    time.sleep(0.8)

#Fijamos un FLAG y Scrolleamos hasta ahi ('DESCUENTOS' - Desde 5% OFF)
def test_scrollFlag():
    flag = driver.find_element(By.XPATH,'//*[@id="root-app"]/div/div[1]/aside/form/div[18]/ul/li[1]/button/span[1]')
    driver.execute_script("arguments[0].scrollIntoView();",flag)
    time.sleep(1.5)

#Seleccionamos 'Desde 5% OFF'
def test_5OFF():
    flag = driver.find_element(By.XPATH,'//*[@id="root-app"]/div/div[1]/aside/form/div[18]/ul/li[1]/button/span[1]')
    flag.click()
    time.sleep(1.5)

#Escribimos en la barra de busqueda
def test_search():
    busqueda = driver.find_element(By.CLASS_NAME,'nav-search-input')
    busqueda.click()
    time.sleep(0.5)
    busqueda.send_keys('Antonio ')
    time.sleep(0.5)
    busqueda.send_keys('Rodriguez ')
    time.sleep(0.2)
    busqueda.send_keys('Farias ')
    time.sleep(2)

#Cerramos!!!
def test_closeWindow():
    time.sleep(2)
    driver.close()

###### GRACIAS por ver mi codigo ######