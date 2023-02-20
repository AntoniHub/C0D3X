import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options


options = Options()
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.binary_location = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
driver = webdriver.Edge(executable_path='D:/Drivers/msedgedriver.exe', options = options)


"""Test E2E de la seccion de FAQs - Filtraciones de Datos"""

def test_01_openHelp():
    """Inicializamos el driver, la web de Centro de Ayuda y maximizamos la ventana"""
    driver.get('https://cyberguardian.tawk.help/')
    driver.maximize_window()
    assert 'Cyber Guardian - Preguntas frecuentes' in driver.title
    time.sleep(1)

def test_02_barraDeBusqueda():
    """Hacemos click y tipeamos en la barra de busquedas"""
    barraDeBusqueda = driver.find_element(By.XPATH,'/html/body/div[1]/div/div/header/div/div[2]/div/div/div[1]/input')
    barraDeBusqueda.click()
    time.sleep(0.5)
    barraDeBusqueda.send_keys('Dispositivos')
    time.sleep(2.5)

def test_03_clickOnEquis():
    """Hacemos click en la equis de la barra de busqueda para eliminar los caracteres"""
    equis = driver.find_element(By.XPATH,'/html/body/div[1]/div/div/header/div/div[2]/div/div/div[1]/div/span')
    equis.click()
    time.sleep(0.5)

def test_04_buttonBtn():
    """Hacemos click en el boton de lineas para organizar la categoria de preguntas"""
    buttonBtn = driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div/div/div[1]/button[2]/div')
    buttonBtn.click()
    time.sleep(1.5)

def test_05_buttonBtnActive():
    """Hacemos click en el boton de cuadros para volver a visualizacion por iconos"""
    buttonBtnActive = driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div/div/div[1]/button[1]')
    buttonBtnActive.click()
    time.sleep(1.5)

def test_06_seguridadDispositivos():
    """Hacemmos click en la seccion de Seguridad de Dispositivos y abrimos en otra ventana"""
    driver.execute_script("window.open('');")
    time.sleep(0.5)

    # change window
    driver.switch_to.window(driver.window_handles[1])
    time.sleep(0.5)

    # Open General Category
    driver.get('https://cyberguardian.tawk.help/category/filtraciones-de-datos')
    time.sleep(2.5)
    assert 'Cyber Guardian - Preguntas frecuentes | Filtraciones de datos' in driver.title


def test_07_barraDeBusqueda():
    """Hacemos click e ingresamos caracteres en la barra de busqueda de
    Filtraciones de datos en FAQs"""
    barraBusqueda = driver.find_element(By.XPATH,'/html/body/div[1]/div/div/header/div/div[2]/div/div/div[1]/input')
    barraBusqueda.click()
    time.sleep(1)

    barraBusqueda.send_keys('Factum - CyberGuardian')
    time.sleep(2)

def test_08_equisBarraBusqueda():
    """Hacemos click en la Equis de la barra de busqueda para blanquear los caracteres ingresados"""
    equis = driver.find_element(By.XPATH,'/html/body/div[1]/div/div/header/div/div[2]/div/div/div[1]/div/span')
    equis.click()
    time.sleep(1)

def test_09_item01():
    """Hacemos click en ¿Qué son las filtraciones de datos públicas?"""
    item01 = driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div/div/div[1]/div[2]/div[2]/div/div/div[1]/a/div[2]/div[1]')
    item01.click()
    time.sleep(2)


def test_10_barraBusquedaItem():
    """Hacemos click e ingresamos caracteres en la barra de busqueda dentro de la seccion general"""
    barraBusquedaItem01 = driver.find_element(By.XPATH,'/html/body/div[1]/div/div/header/div/div[2]/div/div/div[1]/input')
    barraBusquedaItem01.click()
    time.sleep(0.5)

    barraBusquedaItem01.send_keys('Factum - CyberGuardian')
    time.sleep(2)


def test_11_equisBarraBusqueda():
    """Hacemos click en la equis de la barra de busqueda dentro de la seccion para blanquear los caracteres"""
    equis = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/header/div/div[2]/div/div/div[1]/div/span')
    equis.click()
    time.sleep(1)

    driver.execute_script("window.scrollTo(0,2000);")
    time.sleep(2)


def test_12_seguridadPaginaWeb():
    """Hacemos click en el link Seguridad Pagina Web para volver a todas las categorias"""
    seguridadPW = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div/div/div/div[1]/div/div[2]/a/span[2]')
    seguridadPW.click()
    time.sleep(2)

def test_13_item02():
    """Hacemos click en ¿Por qué importa si mis empleados se ven afectados en una filtración de datos?"""
    item02 = driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div/div/div[1]/div[2]/div[2]/div/div/div[2]/a/div[2]/div[1]')
    item02.click()
    time.sleep(2)


def test_14_barraBusquedaItem():
    """Hacemos click e ingresamos caracteres en la barra de busqueda dentro de la seccion general"""
    barraBusquedaItem01 = driver.find_element(By.XPATH,
                                              '/html/body/div[1]/div/div/header/div/div[2]/div/div/div[1]/input')
    barraBusquedaItem01.click()
    time.sleep(0.5)

    barraBusquedaItem01.send_keys('Factum - CyberGuardian')
    time.sleep(2)


def test_15_equisBarraBusqueda():
    """Hacemos click en la equis de la barra de busqueda dentro de la seccion para blanquear los caracteres"""
    equis = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/header/div/div[2]/div/div/div[1]/div/span')
    equis.click()
    time.sleep(1)

    driver.execute_script("window.scrollTo(0,2000);")
    time.sleep(2)


def test_16_seguridadPaginaWeb():
    """Hacemos click en el link Seguridad Pagina Web para volver a todas las categorias"""
    seguridadPW = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div/div/div/div[1]/div/div[2]/a/span[2]')
    seguridadPW.click()
    time.sleep(2)

def test_17_item03():
    """hacemos click en ¿Cómo puedo solucionar las filtraciones de datos que afecten a mis empleados?"""
    item03 = driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div/div/div[1]/div[2]/div[2]/div/div/div[3]/a/div[2]/div[1]')
    item03.click()
    time.sleep(2)


def test_18_barraBusquedaItem():
    """Hacemos click e ingresamos caracteres en la barra de busqueda dentro de la seccion general"""
    barraBusquedaItem01 = driver.find_element(By.XPATH,
                                              '/html/body/div[1]/div/div/header/div/div[2]/div/div/div[1]/input')
    barraBusquedaItem01.click()
    time.sleep(0.5)

    barraBusquedaItem01.send_keys('Factum - CyberGuardian')
    time.sleep(2)


def test_19_equisBarraBusqueda():
    """Hacemos click en la equis de la barra de busqueda dentro de la seccion para blanquear los caracteres"""
    equis = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/header/div/div[2]/div/div/div[1]/div/span')
    equis.click()
    time.sleep(1)

    driver.execute_script("window.scrollTo(0,2000);")
    time.sleep(2)


def test_20_seguridadPaginaWeb():
    """Hacemos click en el link Seguridad Pagina Web para volver a todas las categorias"""
    seguridadPW = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div/div/div/div[1]/div/div[2]/a/span[2]')
    seguridadPW.click()
    time.sleep(2)

def test_21_tearDown():
    """Cerramos el driver"""
    driver.quit()