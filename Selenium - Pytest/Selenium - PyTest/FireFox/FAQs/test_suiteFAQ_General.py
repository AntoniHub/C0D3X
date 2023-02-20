import time
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



"""Test E2E de la seccion de FAQs - General"""


def test_01_openHelp():
    """Inicializamos el driver, la web de Centro de Ayuda y maximizamosla ventana"""
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

def test_06_clickOnGeneral():
    """Hacemos click en la categoria general y abrimos en otra ventana"""
    driver.execute_script("window.open('');")
    time.sleep(0.5)

    # change window
    driver.switch_to.window(driver.window_handles[1])
    time.sleep(0.5)

    # Open General Category
    driver.get('https://cyberguardian.tawk.help/category/general')
    time.sleep(1.5)
    assert 'Cyber Guardian - Preguntas frecuentes | General' in driver.title


def test_07_barraDeBusqueda():
    """Hacemos click y escribimos en la barra de busquedas"""
    barraGeneral = driver.find_element(By.XPATH,'/html/body/div[1]/div/div/header/div/div[2]/div/div/div[1]/input')
    barraGeneral.click()
    time.sleep(0.5)

    # Escribimos 2FA en la barra de busqueda
    barraGeneral.send_keys('2FA')
    time.sleep(2)

def test_08_clickOnEquis():
    """Hacemos click en la equis para eliminar la busqueda"""
    equis = driver.find_element(By.XPATH,'/html/body/div[1]/div/div/header/div/div[2]/div/div/div[1]/div/span')
    equis.click()
    time.sleep(1)

def test_09_newEmployee():
    """Hacemos click en el item 01
    ¿Qué debo hacer cuando hay un nuevo empleado o cuando uno de los empleados se va de la empresa?"""
    driver.execute_script("window.open('');")
    time.sleep(0.5)

    # change window
    driver.switch_to.window(driver.window_handles[2])
    time.sleep(0.5)

    # Open item01
    driver.get('https://cyberguardian.tawk.help/article/%C2%BFqu%C3%A9-debo-hacer-cuando-hay-un-nuevo-empleado-o-cuando-uno-de-los-empleados-se-va-de-la-empresa')
    time.sleep(1.5)
    assert 'Cyber Guardian - Preguntas frecuentes | ¿Qué debo hacer cuando hay un nuevo empleado o cuando uno de los empleados se va de la empresa?' in driver.title

    # Scroll to end body
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1)

    # Return to page 1
    driver.close()
    driver.switch_to.window(driver.window_handles[1])
    time.sleep(0.5)

def test_10_calcularPuntuacion():
    """Hacemos click en
    Cyber Guardian - Centro de Ayuda | ¿Cómo se calcula mi puntuación de seguridad?"""
    driver.execute_script("window.open('');")
    time.sleep(0.5)

    # change window
    driver.switch_to.window(driver.window_handles[2])
    time.sleep(0.5)

    # Open item02
    driver.get('https://cyberguardian.tawk.help/article/%C2%BFcomo-se-calcula-mi-puntuaci%C3%B3n-de-seguridad')
    time.sleep(1.5)
    assert 'Cyber Guardian - Preguntas frecuentes | ¿Cómo se calcula mi puntuación de seguridad?' in driver.title

    # Scroll to end body
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1)

    # Return to page 1
    driver.close()
    driver.switch_to.window(driver.window_handles[1])
    time.sleep(0.5)

def test_11_accionesRealizar():
    """HAcemos click en
    ¿Qué acciones debo realizar en primer lugar?"""
    driver.execute_script("window.open('');")
    time.sleep(0.5)

    # change window
    driver.switch_to.window(driver.window_handles[2])
    time.sleep(0.5)

    # Open item03
    driver.get('https://cyberguardian.tawk.help/article/%C2%BFqu%C3%A9-acciones-debo-realizar-en-primer-lugar')
    time.sleep(1.5)
    assert 'Cyber Guardian - Preguntas frecuentes | ¿Qué acciones debo realizar en primer lugar?' in driver.title

    # Scroll to end body
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1)

    # Return to page 1
    driver.close()
    driver.switch_to.window(driver.window_handles[1])
    time.sleep(0.5)

def test_12_navegarPlataforma():
    """Hacemos click en Cómo navegar por la plataforma"""
    driver.execute_script("window.open('');")
    time.sleep(0.5)

    # change window
    driver.switch_to.window(driver.window_handles[2])
    time.sleep(0.5)

    # Open item04
    driver.get('https://cyberguardian.tawk.help/article/c%C3%B3mo-navegar-por-la-plataforma')
    time.sleep(1.5)
    assert 'Cyber Guardian - Preguntas frecuentes | Cómo navegar por la plataforma' in driver.title

    # Scroll to end body
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1)

    # Return to page 1
    driver.close()
    driver.switch_to.window(driver.window_handles[1])
    time.sleep(0.5)

def test_13_comoEmpezar():
    """Hacemos click en ¿Como empezar?"""
    driver.execute_script("window.open('');")
    time.sleep(0.5)

    # change window
    driver.switch_to.window(driver.window_handles[2])
    time.sleep(0.5)

    # Open item05
    driver.get('https://cyberguardian.tawk.help/article/como-empezar')
    time.sleep(1.5)
    assert 'Cyber Guardian - Preguntas frecuentes | Cómo empezar' in driver.title

    # Scroll to end body
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1)

    # Return to page 1
    driver.close()
    driver.switch_to.window(driver.window_handles[1])
    time.sleep(0.5)

def test_14_2FA():
    """Hacemos click en ¿Qué es el 2FA (autenticación de doble factor)?"""
    driver.execute_script("window.open('');")
    time.sleep(0.5)

    # change window
    driver.switch_to.window(driver.window_handles[2])
    time.sleep(0.5)

    # Open item06
    driver.get('https://cyberguardian.tawk.help/article/%C2%BFqu%C3%A9-es-el-2fa-autenticaci%C3%B3n-de-doble-factor')
    time.sleep(1.5)
    assert 'Cyber Guardian - Preguntas frecuentes | ¿Qué es el 2FA (autenticación de doble factor)?' in driver.title

    # Scroll to end body
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1)

    # Return to page 1
    driver.close()
    driver.switch_to.window(driver.window_handles[1])
    time.sleep(2)

    # Return to Page 0
    driver.close()
    driver.switch_to.window(driver.window_handles[0])
    time.sleep(1)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1)

def test_15_tearDown():
    """Cerramos el driver"""
    driver.quit()