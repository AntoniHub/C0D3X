import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary


options = Options()
options.binary = FirefoxBinary(r'C:\Program Files\Mozilla Firefox\firefox.exe')
options.set_preference("browser.download.folderList",2)
options.set_preference("browser.download.manager.showWhenStarting", False)
options.set_preference("browser.download.dir","/Data")
options.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/octet-stream,application/vnd.ms-excel")
driver = webdriver.Firefox(executable_path='D:/Drivers/geckodriver.exe', options=options)


"""Test E2E de la seccion de FAQs - Seguridad de Proveedores"""

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
    driver.get('https://cyberguardian.tawk.help/category/seguridad-de-proveedores')
    time.sleep(2.5)
    assert 'Cyber Guardian - Preguntas frecuentes | Seguridad de proveedores' in driver.title

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
    """Hacemos click en ¿En qué consiste la seguridad de proveedores de Cyber Guardian?"""
    item01 = driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div/div/div[1]/div[2]/div[2]/div/div/div/a/div[2]/div[1]')
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

@pytest.mark.skip(reason="Verify .DOCX")
def test_validartexto():
    titulo = driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div/div/div/div[2]/div[2]/div[1]/div/h1')
    p1 = driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div/div/div/div[2]/div[2]/div[1]/div/div[2]/div')
    p2 = driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div/div/div/div[2]/div[2]/div[1]/div/div[2]/div/p[2]')
    p3 = driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div/div/div/div[2]/div[2]/div[1]/div/div[2]/div/p[3]')
    assert titulo.text == '¿En qué consiste la seguridad de proveedores de Cyber Guardian?'
    assert p1.text == 'Analizamos  la seguridad de las páginas web de tus proveedores y su riesgo de suplantación de identidad por correo electrónico.'
    assert p2.text == 'La seguridad de la página web de tus proveedores te afecta en la medida que tu negocio dependa de la página web del proveedor. Si tu proveedor no aplica ciertas medidas de seguridad a su página web, los ciberdelincuentes podrían atacarla y dejarla inactiva o filtrar los datos que hayas intercambiado con esta página web.'
    assert p3.text == 'La seguridad del correo electrónico de tus proveedores te afecta en la medida que tu negocio intercambia información con ellos por correo electrónico. Si tu proveedor no aplica ciertas medidas de seguridad a la configuración de su correo electrónico, esto puede generar un riesgo de suplantación de la identidad de tu proveedor. Analizamos la configuración de su correo electrónico, para ver si podría ser suplantado fácilmente y sus direcciones de correo electrónico, para ver si están presentes en filtraciones de datos públicas. Si detectamos problemas en este sentido te avisaremos para que tomes precauciones cuando recibas correos electrónicos de ellos, especialmente si te requieren cambios de información de pagos, cuentas bancarias, etc.'


def test_12_seguridadPaginaWeb():
    """Hacemos click en el link Seguridad Pagina Web para volver a todas las categorias"""
    seguridadPW = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div/div/div/div[1]/div/div[2]/a/span[2]')
    seguridadPW.click()
    time.sleep(2)

def test_13_tearDown():
    """Cerramos el driver"""
    driver.quit()