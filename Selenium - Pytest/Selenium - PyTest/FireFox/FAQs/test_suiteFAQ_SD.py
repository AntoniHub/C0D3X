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


"""Test E2E de la seccion de FAQs - Seguridad de Dispositivos"""

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
    driver.get('https://cyberguardian.tawk.help/category/seguridad-de-dispositivos')
    time.sleep(2.5)
    assert 'Cyber Guardian - Preguntas frecuentes | Seguridad de dispositivos' in driver.title


def test_07_barraDeBusqueda():
    """Hacemos click e ingresamos caracteres en la barra de busqueda de
    Seguridad de Dispositivos en FAQs"""
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
    """Hacemos click en ¿Qué incluye la protección frente a amenazas de Cyber Guardian?"""
    item01 = driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div/div/div[1]/div[2]/div[2]/div/div[1]/div[1]/a/div[2]/div[1]')
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
    """HAcemos click en ¿En qué consiste la protección para dispositivos de Cyber Guardian?"""
    item02 = driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div/div/div[1]/div[2]/div[2]/div/div[1]/div[2]/a/div[2]/div[1]')
    item02.click()
    time.sleep(2)

def test_14_barraBusquedaItem():
    """Hacemos click e ingresamos caracteres en la barra de busqueda dentro de la seccion general"""
    barraBusquedaItem01 = driver.find_element(By.XPATH,'/html/body/div[1]/div/div/header/div/div[2]/div/div/div[1]/input')
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
    """Hacemos click en ¿En qué se diferencia la protección de dispositivos Cyber Guardian de un antivirus tradicional?"""
    item03 = driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div/div/div[1]/div[2]/div[2]/div/div[1]/div[3]/a/div[2]/div[1]')
    item03.click()
    time.sleep(2)

def test_18_barraBusquedaItem():
    """Hacemos click e ingresamos caracteres en la barra de busqueda dentro de la seccion general"""
    barraBusquedaItem01 = driver.find_element(By.XPATH,'/html/body/div[1]/div/div/header/div/div[2]/div/div/div[1]/input')
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

def test_21_item04():
    """Hacemos click en ¿Cómo instalo la protección en mis dispositivos?"""
    item04 = driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div/div/div[1]/div[2]/div[2]/div/div[1]/div[4]/a/div[2]/div[1]')
    item04.click()
    time.sleep(2)

def test_22_barraBusquedaItem():
    """Hacemos click e ingresamos caracteres en la barra de busqueda dentro de la seccion general"""
    barraBusquedaItem01 = driver.find_element(By.XPATH,'/html/body/div[1]/div/div/header/div/div[2]/div/div/div[1]/input')
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

def test_25_item05():
    """Hacemos click en ¿En qué consiste la protección de navegación de Cyber Guardian?"""
    item05 = driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div/div/div[1]/div[2]/div[2]/div/div[1]/div[5]/a/div[2]/div[1]')
    item05.click()
    time.sleep(2)

def test_26_barraBusquedaItem():
    """Hacemos click e ingresamos caracteres en la barra de busqueda dentro de la seccion general"""
    barraBusquedaItem01 = driver.find_element(By.XPATH,'/html/body/div[1]/div/div/header/div/div[2]/div/div/div[1]/input')
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

def test_29_item06():
    """Hacemos click en ¿Cómo instalo la protección antimalware y la protección de navegación en mis dispositivos?"""
    item06 = driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div/div/div[1]/div[2]/div[2]/div/div[1]/div[6]/a/div[2]/div[1]')
    item06.click()
    time.sleep(2)

def test_30_barraBusquedaItem():
    """Hacemos click e ingresamos caracteres en la barra de busqueda dentro de la seccion general"""
    barraBusquedaItem01 = driver.find_element(By.XPATH,'/html/body/div[1]/div/div/header/div/div[2]/div/div/div[1]/input')
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

def test_33_item07():
    """HAcemos click en ¿En qué consiste el servicio de vigilancia y gestión de alertas proactiva de Cyber Guardian?"""
    item07 = driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div/div/div[1]/div[2]/div[2]/div/div[1]/div[7]/a/div[2]/div[1]')
    item07.click()
    time.sleep(2)

def test_34_barraBusquedaItem():
    """Hacemos click e ingresamos caracteres en la barra de busqueda dentro de la seccion general"""
    barraBusquedaItem01 = driver.find_element(By.XPATH,'/html/body/div[1]/div/div/header/div/div[2]/div/div/div[1]/input')
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

def test_37_item08():
    """Hacemos click en ¿Qué es un sistema operativo?"""
    item08 = driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div/div/div[1]/div[2]/div[2]/div/div[1]/div[8]/a/div[2]/div[1]')
    item08.click()
    time.sleep(2)

def test_38_barraBusquedaItem():
    """Hacemos click e ingresamos caracteres en la barra de busqueda dentro de la seccion general"""
    barraBusquedaItem01 = driver.find_element(By.XPATH,'/html/body/div[1]/div/div/header/div/div[2]/div/div/div[1]/input')
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

def test_41_item09():
    """Hacemos click en ¿Por qué actualizar los sistemas operativos?"""
    item09 = driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div/div/div[1]/div[2]/div[2]/div/div[1]/div[9]/a/div[2]/div[1]')
    item09.click()
    time.sleep(2)

def test_42_barraBusquedaItem():
    """Hacemos click e ingresamos caracteres en la barra de busqueda dentro de la seccion general"""
    barraBusquedaItem01 = driver.find_element(By.XPATH,'/html/body/div[1]/div/div/header/div/div[2]/div/div/div[1]/input')
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

def test_45_item10():
    """Hacemos click en ¿Por qué actualizar los navegadores?"""
    item10 = driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div/div/div[1]/div[2]/div[2]/div/div[1]/div[10]/a/div[2]/div[1]')
    item10.click()
    time.sleep(2)

def test_46_barraBusquedaItem():
    """Hacemos click e ingresamos caracteres en la barra de busqueda dentro de la seccion general"""
    barraBusquedaItem01 = driver.find_element(By.XPATH,'/html/body/div[1]/div/div/header/div/div[2]/div/div/div[1]/input')
    barraBusquedaItem01.click()
    time.sleep(0.5)

    barraBusquedaItem01.send_keys('Factum - CyberGuardian')
    time.sleep(2)

def test_47_equisBarraBusqueda():
    """Hacemos click en la equis de la barra de busqueda dentro de la seccion para blanquear los caracteres"""
    equis = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/header/div/div[2]/div/div/div[1]/div/span')
    equis.click()
    time.sleep(1)

    driver.execute_script("window.scrollTo(0,2000);")
    time.sleep(2)

def test_48_seguridadPaginaWeb():
    """Hacemos click en el link Seguridad Pagina Web para volver a todas las categorias"""
    seguridadPW = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div/div/div/div[1]/div/div[2]/a/span[2]')
    seguridadPW.click()
    time.sleep(2)

def test_49_next():
    """Hacemos click en Next para ver los demas items"""
    next = driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div/div/div[1]/div[2]/div[2]/div/div[2]/div/button[2]/span')
    next.click()
    time.sleep(2)

    driver.execute_script("window.scrollTo(0,0);")
    time.sleep(1)

def test_50_item11():
    """Hacemos click en ¿Por qué actualizar las aplicaciones?"""
    item11 = driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div/div/div[1]/div[2]/div[2]/div/div[1]/div[1]/a/div[2]/div[1]')
    item11.click()
    time.sleep(2)

def test_51_barraBusquedaItem():
    """Hacemos click e ingresamos caracteres en la barra de busqueda dentro de la seccion general"""
    barraBusquedaItem01 = driver.find_element(By.XPATH,'/html/body/div[1]/div/div/header/div/div[2]/div/div/div[1]/input')
    barraBusquedaItem01.click()
    time.sleep(0.5)

    barraBusquedaItem01.send_keys('Factum - CyberGuardian')
    time.sleep(2)

def test_52_equisBarraBusqueda():
    """Hacemos click en la equis de la barra de busqueda dentro de la seccion para blanquear los caracteres"""
    equis = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/header/div/div[2]/div/div/div[1]/div/span')
    equis.click()
    time.sleep(1)

    driver.execute_script("window.scrollTo(0,2000);")
    time.sleep(2)

def test_53_seguridadPaginaWeb():
    """Hacemos click en el link Seguridad Pagina Web para volver a todas las categorias"""
    seguridadPW = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div/div/div/div[1]/div/div[2]/a/span[2]')
    seguridadPW.click()
    time.sleep(2)

def test_54_item12():
    """Hacemos click en Next para ver los demas items"""
    driver.execute_script("window.scrollTo(0,2000);")
    time.sleep(1)

    next = driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div/div/div[1]/div[2]/div[2]/div/div[2]/div/button[2]/span')
    next.click()
    time.sleep(2)

    driver.execute_script("window.scrollTo(0,0);")
    time.sleep(1)

    """Hacemos click en ¿Qué es un firewall?"""
    item12 = driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div/div/div[1]/div[2]/div[2]/div/div[1]/div[2]/a/div[2]/div[1]')
    item12.click()
    time.sleep(2)

def test_55_barraBusquedaItem():
    """Hacemos click e ingresamos caracteres en la barra de busqueda dentro de la seccion general"""
    barraBusquedaItem01 = driver.find_element(By.XPATH,'/html/body/div[1]/div/div/header/div/div[2]/div/div/div[1]/input')
    barraBusquedaItem01.click()
    time.sleep(0.5)

    barraBusquedaItem01.send_keys('Factum - CyberGuardian')
    time.sleep(2)

def test_56_equisBarraBusqueda():
    """Hacemos click en la equis de la barra de busqueda dentro de la seccion para blanquear los caracteres"""
    equis = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/header/div/div[2]/div/div/div[1]/div/span')
    equis.click()
    time.sleep(1)

    driver.execute_script("window.scrollTo(0,2000);")
    time.sleep(2)

def test_57_seguridadPaginaWeb():
    """Hacemos click en el link Seguridad Pagina Web para volver a todas las categorias"""
    seguridadPW = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div/div/div/div[1]/div/div[2]/a/span[2]')
    seguridadPW.click()
    time.sleep(2)

def test_58_item13():
    """Hacemos click en Next para ver los demas items"""
    driver.execute_script("window.scrollTo(0,2000);")
    time.sleep(1)

    next = driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div/div/div[1]/div[2]/div[2]/div/div[2]/div/button[2]/span')
    next.click()
    time.sleep(2)

    driver.execute_script("window.scrollTo(0,0);")
    time.sleep(1)

    """Hacemos click en ¿Qué es el cifrado del dispositivo?"""
    item13 = driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div/div/div[1]/div[2]/div[2]/div/div[1]/div[3]/a/div[2]/div[1]')
    item13.click()
    time.sleep(2)

def test_59_barraBusquedaItem():
    """Hacemos click e ingresamos caracteres en la barra de busqueda dentro de la seccion general"""
    barraBusquedaItem01 = driver.find_element(By.XPATH,'/html/body/div[1]/div/div/header/div/div[2]/div/div/div[1]/input')
    barraBusquedaItem01.click()
    time.sleep(0.5)

    barraBusquedaItem01.send_keys('Factum - CyberGuardian')
    time.sleep(2)

def test_60_equisBarraBusqueda():
    """Hacemos click en la equis de la barra de busqueda dentro de la seccion para blanquear los caracteres"""
    equis = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/header/div/div[2]/div/div/div[1]/div/span')
    equis.click()
    time.sleep(1)

    driver.execute_script("window.scrollTo(0,2000);")
    time.sleep(2)

def test_61_seguridadPaginaWeb():
    """Hacemos click en el link Seguridad Pagina Web para volver a todas las categorias"""
    seguridadPW = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div/div/div/div[1]/div/div[2]/a/span[2]')
    seguridadPW.click()
    time.sleep(2)

def test_62_item14():
    """Hacemos click en Next para ver los demas items"""
    driver.execute_script("window.scrollTo(0,2000);")
    time.sleep(1)

    next = driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div/div/div[1]/div[2]/div[2]/div/div[2]/div/button[2]/span')
    next.click()
    time.sleep(2)

    driver.execute_script("window.scrollTo(0,0);")
    time.sleep(1)

    """Hacemos click en ¿Por qué necesito hacer copias de seguridad?"""
    item14 = driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div/div/div[1]/div[2]/div[2]/div/div[1]/div[4]/a/div[2]/div[1]')
    item14.click()
    time.sleep(2)

def test_63_barraBusquedaItem():
    """Hacemos click e ingresamos caracteres en la barra de busqueda dentro de la seccion general"""
    barraBusquedaItem01 = driver.find_element(By.XPATH,'/html/body/div[1]/div/div/header/div/div[2]/div/div/div[1]/input')
    barraBusquedaItem01.click()
    time.sleep(0.5)

    barraBusquedaItem01.send_keys('Factum - CyberGuardian')
    time.sleep(2)

def test_64_equisBarraBusqueda():
    """Hacemos click en la equis de la barra de busqueda dentro de la seccion para blanquear los caracteres"""
    equis = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/header/div/div[2]/div/div/div[1]/div/span')
    equis.click()
    time.sleep(1)

    driver.execute_script("window.scrollTo(0,2000);")
    time.sleep(2)

def test_65_seguridadPaginaWeb():
    """Hacemos click en el link Seguridad Pagina Web para volver a todas las categorias"""
    seguridadPW = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div/div/div/div[1]/div/div[2]/a/span[2]')
    seguridadPW.click()
    time.sleep(2)

def test_66_item15():
    """Hacemos click en Next para ver los demas items"""
    driver.execute_script("window.scrollTo(0,2000);")
    time.sleep(1)

    next = driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div/div/div[1]/div[2]/div[2]/div/div[2]/div/button[2]/span')
    next.click()
    time.sleep(2)

    driver.execute_script("window.scrollTo(0,0);")
    time.sleep(1)

    """Hacemos click en ¿Qué son las copias de seguridad?"""
    item15 = driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div/div/div[1]/div[2]/div[2]/div/div[1]/div[5]/a/div[2]/div[1]')
    item15.click()
    time.sleep(2)

def test_67_barraBusquedaItem():
    """Hacemos click e ingresamos caracteres en la barra de busqueda dentro de la seccion general"""
    barraBusquedaItem01 = driver.find_element(By.XPATH,'/html/body/div[1]/div/div/header/div/div[2]/div/div/div[1]/input')
    barraBusquedaItem01.click()
    time.sleep(0.5)

    barraBusquedaItem01.send_keys('Factum - CyberGuardian')
    time.sleep(2)

def test_68_equisBarraBusqueda():
    """Hacemos click en la equis de la barra de busqueda dentro de la seccion para blanquear los caracteres"""
    equis = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/header/div/div[2]/div/div/div[1]/div/span')
    equis.click()
    time.sleep(1)

    driver.execute_script("window.scrollTo(0,2000);")
    time.sleep(2)

def test_69_seguridadPaginaWeb():
    """Hacemos click en el link Seguridad Pagina Web para volver a todas las categorias"""
    seguridadPW = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div/div/div/div[1]/div/div[2]/a/span[2]')
    seguridadPW.click()
    time.sleep(2)

def test_70_item16():
    """Hacemos click en Next para ver los demas items"""
    driver.execute_script("window.scrollTo(0,2000);")
    time.sleep(1)

    next = driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div/div/div[1]/div[2]/div[2]/div/div[2]/div/button[2]/span')
    next.click()
    time.sleep(2)

    driver.execute_script("window.scrollTo(0,0);")
    time.sleep(1)

    """Hacemos click en ¿Qué software de protección se va a instalar en los dispositivos?"""
    item16 = driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div/div/div[1]/div[2]/div[2]/div/div[1]/div[6]/a/div[2]/div[1]')
    item16.click()
    time.sleep(2)

def test_71_barraBusquedaItem():
    """Hacemos click e ingresamos caracteres en la barra de busqueda dentro de la seccion general"""
    barraBusquedaItem01 = driver.find_element(By.XPATH,'/html/body/div[1]/div/div/header/div/div[2]/div/div/div[1]/input')
    barraBusquedaItem01.click()
    time.sleep(0.5)

    barraBusquedaItem01.send_keys('Factum - CyberGuardian')
    time.sleep(2)

def test_72_equisBarraBusqueda():
    """Hacemos click en la equis de la barra de busqueda dentro de la seccion para blanquear los caracteres"""
    equis = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/header/div/div[2]/div/div/div[1]/div/span')
    equis.click()
    time.sleep(1)

    driver.execute_script("window.scrollTo(0,2000);")
    time.sleep(2)

def test_73_seguridadPaginaWeb():
    """Hacemos click en el link Seguridad Pagina Web para volver a todas las categorias"""
    seguridadPW = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div/div/div/div[1]/div/div[2]/a/span[2]')
    seguridadPW.click()
    time.sleep(2)

def test_74_item17():
    """Hacemos click en Next para ver los demas items"""
    driver.execute_script("window.scrollTo(0,2000);")
    time.sleep(1)

    next = driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div/div/div[1]/div[2]/div[2]/div/div[2]/div/button[2]/span')
    next.click()
    time.sleep(2)

    driver.execute_script("window.scrollTo(0,0);")
    time.sleep(1)

    """Hacemos click en ¿Cuáles son los requisitos de instalación de Crowdstrike?"""
    item17 = driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div/div/div[1]/div[2]/div[2]/div/div[1]/div[7]/a/div[2]/div[1]')
    item17.click()
    time.sleep(2)

def test_75_barraBusquedaItem():
    """Hacemos click e ingresamos caracteres en la barra de busqueda dentro de la seccion general"""
    barraBusquedaItem01 = driver.find_element(By.XPATH,'/html/body/div[1]/div/div/header/div/div[2]/div/div/div[1]/input')
    barraBusquedaItem01.click()
    time.sleep(0.5)

    barraBusquedaItem01.send_keys('Factum - CyberGuardian')
    time.sleep(2)

def test_76_equisBarraBusqueda():
    """Hacemos click en la equis de la barra de busqueda dentro de la seccion para blanquear los caracteres"""
    equis = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/header/div/div[2]/div/div/div[1]/div/span')
    equis.click()
    time.sleep(1)

    driver.execute_script("window.scrollTo(0,2000);")
    time.sleep(2)

def test_77_seguridadPaginaWeb():
    """Hacemos click en el link Seguridad Pagina Web para volver a todas las categorias"""
    seguridadPW = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div/div/div/div[1]/div/div[2]/a/span[2]')
    seguridadPW.click()
    time.sleep(2)

def test_78_item18():
    """Hacemos click en Next para ver los demas items"""
    driver.execute_script("window.scrollTo(0,2000);")
    time.sleep(1)

    next = driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div/div/div[1]/div[2]/div[2]/div/div[2]/div/button[2]/span')
    next.click()
    time.sleep(2)

    driver.execute_script("window.scrollTo(0,0);")
    time.sleep(1)

    """Hacemos click en ¿Cuáles son los requisitos de instalación de Netskope?"""
    item18 = driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div/div/div[1]/div[2]/div[2]/div/div[1]/div[8]/a/div[2]/div[1]')
    item18.click()
    time.sleep(2)

def test_79_barraBusquedaItem():
    """Hacemos click e ingresamos caracteres en la barra de busqueda dentro de la seccion general"""
    barraBusquedaItem01 = driver.find_element(By.XPATH,'/html/body/div[1]/div/div/header/div/div[2]/div/div/div[1]/input')
    barraBusquedaItem01.click()
    time.sleep(0.5)

    barraBusquedaItem01.send_keys('Factum - CyberGuardian')
    time.sleep(2)

def test_80_equisBarraBusqueda():
    """Hacemos click en la equis de la barra de busqueda dentro de la seccion para blanquear los caracteres"""
    equis = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/header/div/div[2]/div/div/div[1]/div/span')
    equis.click()
    time.sleep(1)

    driver.execute_script("window.scrollTo(0,2000);")
    time.sleep(2)

def test_81_seguridadPaginaWeb():
    """Hacemos click en el link Seguridad Pagina Web para volver a todas las categorias"""
    seguridadPW = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div/div/div/div[1]/div/div[2]/a/span[2]')
    seguridadPW.click()
    time.sleep(2)

def test_82_item19():
    """Hacemos click en Next para ver los demas items"""
    driver.execute_script("window.scrollTo(0,2000);")
    time.sleep(1)

    next = driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div/div/div[1]/div[2]/div[2]/div/div[2]/div/button[2]/span')
    next.click()
    time.sleep(2)

    driver.execute_script("window.scrollTo(0,0);")
    time.sleep(1)

    """Hacemos click en Mi Mac me avisa que Apple no puede comprobar si hay software malicioso en el instalador de Cyber Guardian. ¿Qué tengo que hacer?"""
    item19 = driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div/div/div[1]/div[2]/div[2]/div/div[1]/div[9]/a/div[2]/div[1]')
    item19.click()
    time.sleep(2)

def test_83_barraBusquedaItem():
    """Hacemos click e ingresamos caracteres en la barra de busqueda dentro de la seccion general"""
    barraBusquedaItem01 = driver.find_element(By.XPATH,'/html/body/div[1]/div/div/header/div/div[2]/div/div/div[1]/input')
    barraBusquedaItem01.click()
    time.sleep(0.5)

    barraBusquedaItem01.send_keys('Factum - CyberGuardian')
    time.sleep(2)


def test_84_equisBarraBusqueda():
    """Hacemos click en la equis de la barra de busqueda dentro de la seccion para blanquear los caracteres"""
    equis = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/header/div/div[2]/div/div/div[1]/div/span')
    equis.click()
    time.sleep(1)

    driver.execute_script("window.scrollTo(0,2000);")
    time.sleep(2)


def test_85_seguridadPaginaWeb():
    """Hacemos click en el link Seguridad Pagina Web para volver a todas las categorias"""
    seguridadPW = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div/div/div/div[1]/div/div[2]/a/span[2]')
    seguridadPW.click()
    time.sleep(2)

def test_86_previous():
    """Hacemos click en Previous"""
    driver.execute_script("window.scrollTo(0,2000);")
    time.sleep(1)

    next = driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div/div/div[1]/div[2]/div[2]/div/div[2]/div/button[2]/span')
    next.click()
    time.sleep(2)

    previous = driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div/div/div[1]/div[2]/div[2]/div/div[2]/div/button[1]/span')
    previous.click()
    time.sleep(2)

    driver.execute_script("window.scrollTo(0,0);")

def test_87_tearDown():
    """Cerramos el driver"""
    driver.quit()