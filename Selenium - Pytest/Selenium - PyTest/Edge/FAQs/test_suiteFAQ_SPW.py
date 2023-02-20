import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options


options = Options()
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.binary_location = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
driver = webdriver.Edge(executable_path='D:/Drivers/msedgedriver.exe', options = options)


"""Test E2E de la seccion de FAQs - Seguridad de Pagina WEB"""


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
    driver.get('https://cyberguardian.tawk.help/category/seguridad-de-p%C3%A1gina-web')
    time.sleep(1.5)
    assert 'Cyber Guardian - Preguntas frecuentes | Seguridad de página web' in driver.title

def test_07_barraDeBusqueda():
    """Hacemos click e ingresamos caracteres en la barra de busqueda de
    Seguridad de Pagina WEB en FAQs"""
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
    """Hacemos click y abrimos en otro tab la seccion de
    ¿En qué consiste la seguridad de páginas web de Cyber Guardian?"""
    item01 = driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div/div/div[1]/div[2]/div[2]/div/div[1]/div[1]/a/div[2]/div[1]')
    item01.click()
    #assert 'Cyber Guardian - Centro de Ayuda | ¿En qué consiste la seguridad de páginas web de Cyber Guardian?' in driver.title
    time.sleep(3)

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
    """Hacemos click en la seccion ¿Qué es la suplantación de páginas web?"""
    item02 = driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div/div/div[1]/div[2]/div[2]/div/div[1]/div[2]/a/div[2]/div[1]')
    item02.click()
    #assert 'Cyber Guardian - Centro de Ayuda | ¿Qué es la suplantación de páginas web?' in driver.title
    time.sleep(2.5)

def test_14_barraBusqueda():
    """Hacemos click en la barra de busqueda e ingresamos caracteres"""
    barraBusqueda = driver.find_element(By.XPATH,'/html/body/div[1]/div/div/header/div/div[2]/div/div/div[1]/input')
    barraBusqueda.click()
    time.sleep(0.5)

    barraBusqueda.send_keys('Factum - CyberGuardian')
    time.sleep(2)

def test_15_equis():
    """Hacemos click en la equis para blanquear los caracteres ingresados"""
    equis = driver.find_element(By.XPATH,'/html/body/div[1]/div/div/header/div/div[2]/div/div/div[1]/div/span')
    equis.click()
    time.sleep(0.5)

    driver.execute_script("window.scrollTo(0,2000);")
    time.sleep(2)

def test_16_seguridadPaginaWeb():
    """Hacemos click en el link Seguridad Pagina Web para volver a todas las categorias"""
    seguridadPW = driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div/div/div/div[1]/div/div[2]/a/span[2]')
    seguridadPW.click()
    time.sleep(2.5)

def test_17_item03():
    """Hacemos click en la seccion de ¿En qué consisten los ataques de cross site scripting (XSS)?"""
    scriptingXSS = driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div/div/div[1]/div[2]/div[2]/div/div[1]/div[3]/a/div[2]/div[1]')
    scriptingXSS.click()
    #assert 'Cyber Guardian - Centro de Ayuda | ¿En qué consisten los ataques de cross site scripting (XSS)?' in driver.title
    time.sleep(2.5)

def test_18_barraBusqueda():
    """Hacemos click e ingresamos texto en la barra de busqueda"""
    barraBusqueda = driver.find_element(By.XPATH,'/html/body/div[1]/div/div/header/div/div[2]/div/div/div[1]/input')
    barraBusqueda.click()
    time.sleep(0.5)

    barraBusqueda.send_keys('Factum - CyberGuardian')
    time.sleep(2)

def test_19_equis():
    """Hacemos click en la equis de la barra de busqueda para blanquear los caracteres ingresados"""
    equis = driver.find_element(By.XPATH,'/html/body/div[1]/div/div/header/div/div[2]/div/div/div[1]/div/span')
    equis.click()
    time.sleep(0.5)

    driver.execute_script("window.scrollTo(0,2000);")
    time.sleep(2)

def test_20_seguridadPaginaWeb():
    """Hacemos click en el link Seguridad Pagina Web para volver a todas las categorias"""
    seguridadPW = driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div/div/div/div[1]/div/div[2]/a/span[2]')
    seguridadPW.click()
    time.sleep(2.5)

def test_21_item04():
    """Hacemos click en Cyber Guardian - Centro de Ayuda | ¿Por qué necesito protección contra el cross site scripting (XXS)?"""
    item04 = driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div/div/div[1]/div[2]/div[2]/div/div[1]/div[4]/a/div[2]/div[1]')
    item04.click()
    #assert 'Cyber Guardian - Centro de Ayuda | ¿Por qué necesito protección contra el cross site scripting (XXS)?' in driver.title
    time.sleep(2.5)

def test_22_barraBusqueda():
    """Hacemos click e ingresamos etexto en la barra de busqueda de la seccion"""
    barraBusqueda = driver.find_element(By.XPATH,'/html/body/div[1]/div/div/header/div/div[2]/div/div/div[1]/input')
    barraBusqueda.click()
    time.sleep(0.5)

    barraBusqueda.send_keys('Factum - CyberGuardian')
    time.sleep(2)

def test_23_equis():
    """HAcemos click en la equis para blanquear los caracteres ingresados en la barra de busqueda"""
    equis = driver.find_element(By.XPATH,'/html/body/div[1]/div/div/header/div/div[2]/div/div/div[1]/div/span')
    equis.click()
    time.sleep(1)

    driver.execute_script("window.scrollTo(0,2000);")
    time.sleep(2)

def test_24_seguridadPaginaWeb():
    """Hacemos click en el link Seguridad Pagina Web para volver a todas las categorias"""
    seguridadPW = driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div/div/div/div[1]/div/div[2]/a/span[2]')
    seguridadPW.click()
    time.sleep(2.5)

def test_25_item05():
    """Hacemos click en la seccion ¿Cómo me puedo proteger del cross-site scripting (XXS)?"""
    item05 = driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div/div/div[1]/div[2]/div[2]/div/div[1]/div[5]/a/div[2]/div[1]')
    item05.click()
    #assert 'Cyber Guardian - Centro de Ayuda | ¿Cómo me puedo proteger del cross-site scripting (XXS)?' in driver.title
    time.sleep(2.5)

def test_26_barraBusqueda():
    """Hacemos click en la barra de busqueda e ingresamos cadena de caracteres"""
    barraBusqueda = driver.find_element(By.XPATH,'/html/body/div[1]/div/div/header/div/div[2]/div/div/div[1]/input')
    barraBusqueda.click()
    time.sleep(0.5)

    barraBusqueda.send_keys('Factum - CyberGuardian')
    time.sleep(2)

def test_27_equis():
    """Hacemos click en la equis para blanquear los caracteres ingresados"""
    equis = driver.find_element(By.XPATH,'/html/body/div[1]/div/div/header/div/div[2]/div/div/div[1]/div/span')
    equis.click()
    time.sleep(0.5)

    driver.execute_script("window.scrollTo(0,2000);")
    time.sleep(2)

def test_28_seguridadPaginaWeb():
    """Hacemos click en el link Seguridad Pagina Web para volver a todas las categorias"""
    seguridadPW = driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div/div/div/div[1]/div/div[2]/a/span[2]')
    seguridadPW.click()
    time.sleep(2.5)

def test_29_item06():
    """Hacemos click en ¿En qué consisten los ataques de clickjacking?"""
    item06 = driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div/div/div[1]/div[2]/div[2]/div/div[1]/div[6]/a/div[2]/div[1]')
    item06.click()
    time.sleep(2)

def test_30_barraBusqueda():
    """Hacemos click en la barra de busqueda e ingresamos texto"""
    barraBusqueda = driver.find_element(By.XPATH,'/html/body/div[1]/div/div/header/div/div[2]/div/div/div[1]/input')
    barraBusqueda.click()
    time.sleep(1)

    barraBusqueda.send_keys('Factum - CyberGuardian')
    time.sleep(2)

def test_31_equis():
    """Hacemos click en la equis para blanquear los datos ingresados"""
    equis = driver.find_element(By.XPATH,'/html/body/div[1]/div/div/header/div/div[2]/div/div/div[1]/div/span')
    equis.click()
    time.sleep(1)

    driver.execute_script("window.scrollTo(0,2000);")
    time.sleep(2)

def test_32_seguridadPaginaWeb():
    """Hacemos click en el link Seguridad Pagina Web para volver a todas las categorias"""
    seguridadPW = driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div/div/div/div[1]/div/div[2]/a/span[2]')
    seguridadPW.click()
    time.sleep(2.5)

def test_33_item07():
    """HAcemos click en ¿Cómo me puedo proteger del clickjacking?"""
    item07 = driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div/div/div[1]/div[2]/div[2]/div/div[1]/div[7]/a/div[2]/div[1]')
    item07.click()
    time.sleep(2.5)

def test_34_barraBusqueda():
    """Hacemos click en la barra de busqueda e ingresamos texto"""
    barraBusqueda = driver.find_element(By.XPATH,'/html/body/div[1]/div/div/header/div/div[2]/div/div/div[1]/input')
    barraBusqueda.click()
    time.sleep(1)

    barraBusqueda.send_keys('Factum - CyberGuardian')
    time.sleep(2)

def test_35_equis():
    """HAcemos click en la equis para blanquear los datos ingresados"""
    equis = driver.find_element(By.XPATH,'/html/body/div[1]/div/div/header/div/div[2]/div/div/div[1]/div/span')
    equis.click()
    time.sleep(1)

    driver.execute_script("window.scrollTo(0,2000);")
    time.sleep(2)

def test_36_seguridadPaginaWeb():
    """Hacemos click en el link Seguridad Pagina Web para volver a todas las categorias"""
    seguridadPW = driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div/div/div/div[1]/div/div[2]/a/span[2]')
    seguridadPW.click()
    time.sleep(2.5)

    driver.execute_script("window.scrollTo(0,2000);")
    time.sleep(2)

def test_37_item08():
    """Hacemos click en ¿En qué consisten los ataques de intermediario (Man in the middle)?"""
    item08 = driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div/div/div[1]/div[2]/div[2]/div/div[1]/div[8]/a/div[2]/div[1]')
    item08.click()
    time.sleep(2.5)

def test_38_barraBusqueda():
    """Hacemos click en la barra de busqueda e ingresamos texto"""
    barraBusqueda = driver.find_element(By.XPATH,'/html/body/div[1]/div/div/header/div/div[2]/div/div/div[1]/input')
    barraBusqueda.click()
    time.sleep(1)

    barraBusqueda.send_keys('Factum - CyberGuardian')
    time.sleep(2)

def test_39_equis():
    """HAcemos click en la equis para blanquear los datos ingresados"""
    equis = driver.find_element(By.XPATH,'/html/body/div[1]/div/div/header/div/div[2]/div/div/div[1]/div/span')
    equis.click()
    time.sleep(1)

    driver.execute_script("window.scrollTo(0,2000);")
    time.sleep(2)

def test_40_seguridadPaginaWeb():
    """Hacemos click en el link Seguridad Pagina Web para volver a todas las categorias"""
    seguridadPW = driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div/div/div/div[1]/div/div[2]/a/span[2]')
    seguridadPW.click()
    time.sleep(2.5)

def test_41_item09():
    """HAcemos click en ¿Por qué es importante protegerse frente a ataques de Intermediario?"""
    item09 = driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div/div/div[1]/div[2]/div[2]/div/div[1]/div[9]/a/div[2]/div[1]')
    item09.click()
    time.sleep(2.5)

def test_42_barraBusqueda():
    """Hacemos click en la barra de busqueda e ingresamos texto"""
    barraBusqueda = driver.find_element(By.XPATH,'/html/body/div[1]/div/div/header/div/div[2]/div/div/div[1]/input')
    barraBusqueda.click()
    time.sleep(1)

    barraBusqueda.send_keys('Factum - CyberGuardian')
    time.sleep(2)

def test_43_equis():
    """HAcemos click en la equis para blanquear los datos ingresados"""
    equis = driver.find_element(By.XPATH,'/html/body/div[1]/div/div/header/div/div[2]/div/div/div[1]/div/span')
    equis.click()
    time.sleep(1)

    driver.execute_script("window.scrollTo(0,2000);")
    time.sleep(2)

def test_44_seguridadPaginaWeb():
    """Hacemos click en el link Seguridad Pagina Web para volver a todas las categorias"""
    seguridadPW = driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div/div/div/div[1]/div/div[2]/a/span[2]')
    seguridadPW.click()
    time.sleep(2.5)

def test_45_item10():
    """Hacemos click en ¿Cómo me puedo proteger de los ataques de intermediario?"""
    item10 = driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div/div/div[1]/div[2]/div[2]/div/div[1]/div[10]/a/div[2]/div[1]')
    item10.click()
    time.sleep(2.5)

def test_46_barraBusqueda():
    """Hacemos click en la barra de busqueda e ingresamos texto"""
    barraBusqueda = driver.find_element(By.XPATH,'/html/body/div[1]/div/div/header/div/div[2]/div/div/div[1]/input')
    barraBusqueda.click()
    time.sleep(1)

    barraBusqueda.send_keys('Factum - CyberGuardian')
    time.sleep(2)

def test_47_equis():
    """HAcemos click en la equis para blanquear los datos ingresados"""
    equis = driver.find_element(By.XPATH,'/html/body/div[1]/div/div/header/div/div[2]/div/div/div[1]/div/span')
    equis.click()
    time.sleep(1)

    driver.execute_script("window.scrollTo(0,2000);")
    time.sleep(2)

def test_48_seguridadPaginaWeb():
    """Hacemos click en el link Seguridad Pagina Web para volver a todas las categorias"""
    seguridadPW = driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div/div/div/div[1]/div/div[2]/a/span[2]')
    seguridadPW.click()
    time.sleep(2.5)

def test_49_Next():
    """Hacemos click en el boton Next al final de la pagina para ver las demas secciones de Seguridad de Pagina WEB"""
    next = driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div/div/div[1]/div[2]/div[2]/div/div[2]/div/button[2]/span')
    next.click()
    time.sleep(2.5)

    driver.execute_script("window.scrollTo(0,0);")
    time.sleep(2)

def test_50_item11():
    """Hacemos click en ¿Qué el cifrado SSL?"""
    item11 = driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div/div/div[1]/div[2]/div[2]/div/div[1]/div[1]/a/div[2]/div[1]')
    item11.click()
    time.sleep(2.5)

def test_51_barraBusqueda():
    """Hacemos click en la barra de busqueda e ingresamos texto"""
    barraBusqueda = driver.find_element(By.XPATH,'/html/body/div[1]/div/div/header/div/div[2]/div/div/div[1]/input')
    barraBusqueda.click()
    time.sleep(1)

    barraBusqueda.send_keys('Factum - CyberGuardian')
    time.sleep(2)

def test_52_equis():
    """HAcemos click en la equis para blanquear los datos ingresados"""
    equis = driver.find_element(By.XPATH,'/html/body/div[1]/div/div/header/div/div[2]/div/div/div[1]/div/span')
    equis.click()
    time.sleep(1)

    driver.execute_script("window.scrollTo(0,2000);")
    time.sleep(2)

def test_53_seguridadPaginaWeb():
    """Hacemos click en el link Seguridad Pagina Web para volver a todas las categorias"""
    seguridadPW = driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div/div/div/div[1]/div/div[2]/a/span[2]')
    seguridadPW.click()
    time.sleep(2.5)

def test_54_Next():
    """Hacemos click en el boton Next al final de la pagina para ver las demas secciones de Seguridad de Pagina WEB"""
    next = driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div/div/div[1]/div[2]/div[2]/div/div[2]/div/button[2]/span')
    next.click()
    time.sleep(2.5)

    driver.execute_script("window.scrollTo(0,0);")
    time.sleep(2)

def test_55_item12():
    """Hacemos click en ¿Cómo puedo implementar el cifrado SSL?"""
    item12 = driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div/div/div[1]/div[2]/div[2]/div/div[1]/div[2]/a/div[2]/div[1]')
    item12.click()
    time.sleep(2.5)

def test_56_barraBusqueda():
    """Hacemos click en la barra de busqueda e ingresamos texto"""
    barraBusqueda = driver.find_element(By.XPATH,'/html/body/div[1]/div/div/header/div/div[2]/div/div/div[1]/input')
    barraBusqueda.click()
    time.sleep(1)

    barraBusqueda.send_keys('Factum - CyberGuardian')
    time.sleep(2)

def test_57_equis():
    """HAcemos click en la equis para blanquear los datos ingresados"""
    equis = driver.find_element(By.XPATH,'/html/body/div[1]/div/div/header/div/div[2]/div/div/div[1]/div/span')
    equis.click()
    time.sleep(1)

    driver.execute_script("window.scrollTo(0,2000);")
    time.sleep(2)

def test_58_seguridadPaginaWeb():
    """Hacemos click en el link Seguridad Pagina Web para volver a todas las categorias"""
    seguridadPW = driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div/div/div/div[1]/div/div[2]/a/span[2]')
    seguridadPW.click()
    time.sleep(2.5)

def test_59_Next():
    """Hacemos click en el boton Next al final de la pagina para ver las demas secciones de Seguridad de Pagina WEB"""
    next = driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div/div/div[1]/div[2]/div[2]/div/div[2]/div/button[2]/span')
    next.click()
    time.sleep(2.5)

    driver.execute_script("window.scrollTo(0,0);")
    time.sleep(2)

def test_60_item13():
    """Hacemos click en ¿En qué consisten los ataques de denegación de servicio (DDoS)?"""
    item13 = driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div/div/div[1]/div[2]/div[2]/div/div[1]/div[3]/a/div[2]/div[1]')
    item13.click()
    time.sleep(2.5)

def test_61_barraBusqueda():
    """Hacemos click en la barra de busqueda e ingresamos texto"""
    barraBusqueda = driver.find_element(By.XPATH,'/html/body/div[1]/div/div/header/div/div[2]/div/div/div[1]/input')
    barraBusqueda.click()
    time.sleep(1)

    barraBusqueda.send_keys('Factum - CyberGuardian')
    time.sleep(2)

def test_62_equis():
    """HAcemos click en la equis para blanquear los datos ingresados"""
    equis = driver.find_element(By.XPATH,'/html/body/div[1]/div/div/header/div/div[2]/div/div/div[1]/div/span')
    equis.click()
    time.sleep(1)

    driver.execute_script("window.scrollTo(0,2000);")
    time.sleep(2)

def test_63_seguridadPaginaWeb():
    """Hacemos click en el link Seguridad Pagina Web para volver a todas las categorias"""
    seguridadPW = driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div/div/div/div[1]/div/div[2]/a/span[2]')
    seguridadPW.click()
    time.sleep(2.5)

def test_64_Next():
    """Hacemos click en el boton Next al final de la pagina para ver las demas secciones de Seguridad de Pagina WEB"""
    next = driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div/div/div[1]/div[2]/div[2]/div/div[2]/div/button[2]/span')
    next.click()
    time.sleep(2.5)

    driver.execute_script("window.scrollTo(0,0);")
    time.sleep(2)

def test_65_item14():
    """Hacemos click en ¿Cómo me puedo proteger de los ataques de denegación de servicio?"""
    item14 = driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div/div/div[1]/div[2]/div[2]/div/div[1]/div[4]/a/div[2]/div[1]')
    item14.click()
    time.sleep(2.5)

def test_66_barraBusqueda():
    """Hacemos click en la barra de busqueda e ingresamos texto"""
    barraBusqueda = driver.find_element(By.XPATH,'/html/body/div[1]/div/div/header/div/div[2]/div/div/div[1]/input')
    barraBusqueda.click()
    time.sleep(1)

    barraBusqueda.send_keys('Factum - CyberGuardian')
    time.sleep(2)

def test_64_equis():
    """HAcemos click en la equis para blanquear los datos ingresados"""
    equis = driver.find_element(By.XPATH,'/html/body/div[1]/div/div/header/div/div[2]/div/div/div[1]/div/span')
    equis.click()
    time.sleep(1)

    driver.execute_script("window.scrollTo(0,2000);")
    time.sleep(2)

def test_67_seguridadPaginaWeb():
    """Hacemos click en el link Seguridad Pagina Web para volver a todas las categorias"""
    seguridadPW = driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div/div/div/div[1]/div/div[2]/a/span[2]')
    seguridadPW.click()
    time.sleep(2.5)

    driver.execute_script("window.scrollTo(0,2000);")
    time.sleep(2)

def test_68_Next():
    """Hacemos click en el boton Next al final de la pagina para ver las demas secciones de Seguridad de Pagina WEB"""
    next = driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div/div/div[1]/div[2]/div[2]/div/div[2]/div/button[2]/span')
    next.click()
    time.sleep(2.5)

    driver.execute_script("window.scrollTo(0,0);")
    time.sleep(1)

    driver.execute_script("window.scrollTo(0,2000);")
    time.sleep(1)

def test_69_Previous():
    """Hacemos click en Previous en la parte inferior de la pantalla para devolver a las categorias de la seccion"""
    previous = driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div/div/div[1]/div[2]/div[2]/div/div[2]/div/button[1]/span')
    previous.click()
    time.sleep(2.5)



def test_70_tearDown():
    """Cerramos el driver"""
    driver.quit()