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


"""Test E2E de la seccion de FAQs - Seguridad de EMails"""

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

def test_06_seguridadEmails():
    """Hacemmos click en la seccion de Seguridad de Emails y abrimos en otra ventana"""
    driver.execute_script("window.open('');")
    time.sleep(0.5)

    # change window
    driver.switch_to.window(driver.window_handles[1])
    time.sleep(0.5)

    # Open General Category
    driver.get('https://cyberguardian.tawk.help/category/seguridad-de-email')
    time.sleep(2.5)
    assert 'Cyber Guardian - Preguntas frecuentes | Seguridad de email' in driver.title

def test_07_barraDeBusqueda():
    """Hacemos click e ingresamos caracteres en la barra de busqueda de
    Seguridad de Emails en FAQs"""
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
    """HAcemos click en ¿En qué consiste la protección de correo electrónico de Cyber Guardian?"""
    item01 = driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div/div/div[1]/div[2]/div[2]/div/div/div[1]/a/div[2]/div[1]')
    item01.click()
    time.sleep(2)

def test_10_barraBusquedaItem01():
    """Hacemos click e ingresamos caracteres en la barra de busqueda dentro de la seccion
    ¿En qué consiste la seguridad de páginas web de Cyber Guardian?"""
    barraBusquedaItem01 = driver.find_element(By.XPATH,'/html/body/div[1]/div/div/header/div/div[2]/div/div/div[1]/input')
    barraBusquedaItem01.click()
    time.sleep(0.5)

    barraBusquedaItem01.send_keys('Factum - CyberGuardian')
    time.sleep(2)

def test_11_equisBarraBusqueda():
    """Hacemos click en la equis de la barra de busqueda dentro de la seccion para blanquear los caracteres"""
    equis = driver.find_element(By.XPATH,'/html/body/div[1]/div/div/header/div/div[2]/div/div/div[1]/div/span')
    equis.click()
    time.sleep(1)

    driver.execute_script("window.scrollTo(0,2000);")
    time.sleep(2)

def test_12_seguridadPaginaWeb():
    """Hacemos click en el link Seguridad Pagina Web para volver a todas las categorias"""
    seguridadPW = driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div/div/div/div[1]/div/div[2]/a/span[2]')
    seguridadPW.click()
    time.sleep(2)

def test_13_item02():
    """Hacemos click en ¿Cómo activo la protección de correo de Cyber Guardian para mi dominio de correo?"""
    item02 = driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div/div/div[1]/div[2]/div[2]/div/div/div[2]/a/div[2]/div[1]')
    item02.click()
    time.sleep(2)

def test_14_barraBusquedaItem():
    """Hacemos click e ingresamos caracteres en la barra de busqueda dentro de la seccion
    ¿En qué consiste la seguridad de páginas web de Cyber Guardian?"""
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
    """Hacemos click en ¿Qué es la cuarentena de emails?"""
    item02 = driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div/div/div[1]/div[2]/div[2]/div/div/div[3]/a/div[2]/div[1]')
    item02.click()
    time.sleep(2)

def test_18_barraBusquedaItem():
    """Hacemos click e ingresamos caracteres en la barra de busqueda dentro de la seccion
    ¿En qué consiste la seguridad de páginas web de Cyber Guardian?"""
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

def test_21_item03():
    """Hacemos click en ¿Cómo gestiono los emails en cuarentena?"""
    item03 = driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div/div/div[1]/div[2]/div[2]/div/div/div[4]/a/div[2]/div[1]')
    item03.click()
    time.sleep(2)

def test_22_barraBusquedaItem():
    """Hacemos click e ingresamos caracteres en la barra de busqueda dentro de la seccion
    ¿En qué consiste la seguridad de páginas web de Cyber Guardian?"""
    barraBusquedaItem01 = driver.find_element(By.XPATH,
                                              '/html/body/div[1]/div/div/header/div/div[2]/div/div/div[1]/input')
    barraBusquedaItem01.click()
    time.sleep(0.5)

    barraBusquedaItem01.send_keys('Factum - CyberGuardian')
    time.sleep(2)

def test_23_equisBarraBusqueda():
    """Hacemos click en la equis de la barra de busqueda dentro de la seccion para blanquear los caracteres"""
    equis = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/header/div/div[2]/div/div/div[1]/div/span')
    equis.click()
    time.sleep(1)

    driver.execute_script("window.scrollTo(0,2000);")
    time.sleep(2)

def test_24_seguridadPaginaWeb():
    """Hacemos click en el link Seguridad Pagina Web para volver a todas las categorias"""
    seguridadPW = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div/div/div/div[1]/div/div[2]/a/span[2]')
    seguridadPW.click()
    time.sleep(2)

def test_25_item04():
    """Hacemos click en ¿Qué es el email spoofing (suplantación de identidad por correo electrónico)?"""
    item04 = driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div/div/div[1]/div[2]/div[2]/div/div/div[5]/a/div[2]/div[1]')
    item04.click()
    time.sleep(2)

def test_26_barraBusquedaItem():
    """Hacemos click e ingresamos caracteres en la barra de busqueda dentro de la seccion
    ¿En qué consiste la seguridad de páginas web de Cyber Guardian?"""
    barraBusquedaItem01 = driver.find_element(By.XPATH,
                                              '/html/body/div[1]/div/div/header/div/div[2]/div/div/div[1]/input')
    barraBusquedaItem01.click()
    time.sleep(0.5)

    barraBusquedaItem01.send_keys('Factum - CyberGuardian')
    time.sleep(2)

def test_27_equisBarraBusqueda():
    """Hacemos click en la equis de la barra de busqueda dentro de la seccion para blanquear los caracteres"""
    equis = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/header/div/div[2]/div/div/div[1]/div/span')
    equis.click()
    time.sleep(1)

    driver.execute_script("window.scrollTo(0,2000);")
    time.sleep(2)

def test_28_seguridadPaginaWeb():
    """Hacemos click en el link Seguridad Pagina Web para volver a todas las categorias"""
    seguridadPW = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div/div/div/div[1]/div/div[2]/a/span[2]')
    seguridadPW.click()
    time.sleep(2)

def test_29_item05():
    """HAcemos click en ¿Qué es SPF?"""
    item05 = driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div/div/div[1]/div[2]/div[2]/div/div/div[6]/a/div[2]/div[1]')
    item05.click()
    time.sleep(2)

def test_30_barraBusquedaItem():
    """Hacemos click e ingresamos caracteres en la barra de busqueda dentro de la seccion
    ¿En qué consiste la seguridad de páginas web de Cyber Guardian?"""
    barraBusquedaItem01 = driver.find_element(By.XPATH,
                                              '/html/body/div[1]/div/div/header/div/div[2]/div/div/div[1]/input')
    barraBusquedaItem01.click()
    time.sleep(0.5)

    barraBusquedaItem01.send_keys('Factum - CyberGuardian')
    time.sleep(2)

def test_31_equisBarraBusqueda():
    """Hacemos click en la equis de la barra de busqueda dentro de la seccion para blanquear los caracteres"""
    equis = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/header/div/div[2]/div/div/div[1]/div/span')
    equis.click()
    time.sleep(1)

    driver.execute_script("window.scrollTo(0,2000);")
    time.sleep(2)

def test_32_seguridadPaginaWeb():
    """Hacemos click en el link Seguridad Pagina Web para volver a todas las categorias"""
    seguridadPW = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div/div/div/div[1]/div/div[2]/a/span[2]')
    seguridadPW.click()
    time.sleep(2)

def test_33_item06():
    """HAcemos click en ¿Qué es DMARC?"""
    item06 = driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div/div/div[1]/div[2]/div[2]/div/div/div[7]/a/div[2]/div[1]')
    item06.click()
    time.sleep(2)

def test_34_barraBusquedaItem():
    """Hacemos click e ingresamos caracteres en la barra de busqueda dentro de la seccion
    ¿En qué consiste la seguridad de páginas web de Cyber Guardian?"""
    barraBusquedaItem01 = driver.find_element(By.XPATH,
                                              '/html/body/div[1]/div/div/header/div/div[2]/div/div/div[1]/input')
    barraBusquedaItem01.click()
    time.sleep(0.5)

    barraBusquedaItem01.send_keys('Factum - CyberGuardian')
    time.sleep(2)

def test_35_equisBarraBusqueda():
    """Hacemos click en la equis de la barra de busqueda dentro de la seccion para blanquear los caracteres"""
    equis = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/header/div/div[2]/div/div/div[1]/div/span')
    equis.click()
    time.sleep(1)

    driver.execute_script("window.scrollTo(0,2000);")
    time.sleep(2)

def test_36_seguridadPaginaWeb():
    """Hacemos click en el link Seguridad Pagina Web para volver a todas las categorias"""
    seguridadPW = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div/div/div/div[1]/div/div[2]/a/span[2]')
    seguridadPW.click()
    time.sleep(2)

def test_37_item07():
    """Hacemos click en ¿Por qué necesito 2FA (autenticación de doble factor) para los emails de mi organización?"""
    item07 = driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div/div/div[1]/div[2]/div[2]/div/div/div[8]/a/div[2]/div[1]')
    item07.click()
    time.sleep(2)

def test_38_barraBusquedaItem():
    """Hacemos click e ingresamos caracteres en la barra de busqueda dentro de la seccion
    ¿En qué consiste la seguridad de páginas web de Cyber Guardian?"""
    barraBusquedaItem01 = driver.find_element(By.XPATH,
                                              '/html/body/div[1]/div/div/header/div/div[2]/div/div/div[1]/input')
    barraBusquedaItem01.click()
    time.sleep(0.5)

    barraBusquedaItem01.send_keys('Factum - CyberGuardian')
    time.sleep(2)

def test_39_equisBarraBusqueda():
    """Hacemos click en la equis de la barra de busqueda dentro de la seccion para blanquear los caracteres"""
    equis = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/header/div/div[2]/div/div/div[1]/div/span')
    equis.click()
    time.sleep(1)

    driver.execute_script("window.scrollTo(0,2000);")
    time.sleep(2)

def test_40_seguridadPaginaWeb():
    """Hacemos click en el link Seguridad Pagina Web para volver a todas las categorias"""
    seguridadPW = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div/div/div/div[1]/div/div[2]/a/span[2]')
    seguridadPW.click()
    time.sleep(2)

def test_41_item08():
    """Hacemos click en ¿Cómo puedo revisar si 2FA (autenticación de doble factor) está activada centralmente para el correo corporativo de mi empresa?"""
    item08 = driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div/div/div[1]/div[2]/div[2]/div/div/div[9]/a/div[2]/div[1]')
    item08.click()
    time.sleep(2)

def test_42_barraBusquedaItem():
    """Hacemos click e ingresamos caracteres en la barra de busqueda dentro de la seccion
    ¿En qué consiste la seguridad de páginas web de Cyber Guardian?"""
    barraBusquedaItem01 = driver.find_element(By.XPATH,
                                              '/html/body/div[1]/div/div/header/div/div[2]/div/div/div[1]/input')
    barraBusquedaItem01.click()
    time.sleep(0.5)

    barraBusquedaItem01.send_keys('Factum - CyberGuardian')
    time.sleep(2)

def test_43_equisBarraBusqueda():
    """Hacemos click en la equis de la barra de busqueda dentro de la seccion para blanquear los caracteres"""
    equis = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/header/div/div[2]/div/div/div[1]/div/span')
    equis.click()
    time.sleep(1)

    driver.execute_script("window.scrollTo(0,2000);")
    time.sleep(2)

def test_44_seguridadPaginaWeb():
    """Hacemos click en el link Seguridad Pagina Web para volver a todas las categorias"""
    seguridadPW = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div/div/div/div[1]/div/div[2]/a/span[2]')
    seguridadPW.click()
    time.sleep(2)

    driver.execute_script("window.scrollTo(0,2000);")
    time.sleep(1)

    driver.execute_script("window.scrollTo(0,0);")
    time.sleep(2)


def test_45_tearDown():
    """Cerramos el driver"""
    driver.quit()