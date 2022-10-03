import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


options = Options()
options.add_argument('--incognito')
options.add_argument('--start-maximized')
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.binary_location = 'C:/Program Files/Google/Chrome/Application/chrome.exe'
dc = DesiredCapabilities.CHROME
dc['goog:loggingPrefs'] = {'browser':'ALL'}
driver = webdriver.Chrome(chrome_options=options, executable_path='D:/Drivers/chromedriver.exe', desired_capabilities=dc)
time.sleep(0.5)


"""
Automatizaremos el Front de Selenium Easy a traves del cual veremos 
las distintas secciones utilizando las librerias llamadas anteriormente
"""

def test_01_HomePage():
    """Abrimos la web, utilizamos un assert para verificar el titulo y capturamos LOGs"""
    driver.get('https://www.seleniumeasy.com/')
    driver.maximize_window()
    assert 'Learn Selenium with Best Practices and Examples | Selenium Easy' in driver.title
    time.sleep(1)

    for e in driver.get_log('browser'):
        print(e)

def test_02_seleniumSeccion():
    """Hacemos click en la seccion Selenium e iteramos sus items invocando ActionChains"""
    selenium = driver.find_element(By.XPATH,'/html/body/header/div/div[2]/nav/ul/li[2]/a/span')
    selenium.click()
    time.sleep(1)

    """Inicializamos ActionChains en la variable action"""
    action = ActionChains(driver)

    """Desplazamos por los items de la seccion Selenium"""
    seleniumWithJava = driver.find_element(By.XPATH,'/html/body/header/div/div[2]/nav/ul/li[2]/ul/li[1]/a')
    action.move_to_element(seleniumWithJava).perform()
    time.sleep(0.6)

    seleniumWithPython = driver.find_element(By.XPATH,'/html/body/header/div/div[2]/nav/ul/li[2]/ul/li[2]/a')
    action.move_to_element(seleniumWithPython).perform()
    time.sleep(0.6)

@pytest.mark.xfail
def test_03_othersSecciones():
    """Hacemos click para visualizar cada una de las otras secciones presentes en la pagina"""
    TestNG = driver.find_element(By.XPATH,'/html/body/header/div/div[2]/nav/ul/li[3]/a')
    TestNG.click()
    time.sleep(2.5)

    #Scrolleamos hasta el final
    driver.execute_script("window.scrollTo(0,2000);")
    time.sleep(1)

    Maven = driver.find_element(By.XPATH,'/html/body/header/div/div[2]/nav/ul/li[4]/a')
    Maven.click()
    time.sleep(2.5)

    #Definimos flag para scrollear
    flag = driver.find_element(By.XPATH,'/html/body/div[3]/div/section/article[6]/header/h2/a')
    driver.execute_script("arguments[0].scrollIntoView();", flag)
    time.sleep(1)

    #Invocamos ActionChains para hacer click
    action = ActionChains(driver)
    Jenkins = driver.find_element(By.XPATH,'/html/body/header/div/div[2]/nav/ul/li[5]/a')
    action.click(on_element=Jenkins)
    time.sleep(2.5)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    Protractor = driver.find_element(By.XPATH,'/html/body/header/div/div[2]/nav/ul/li[6]/a')
    action.click(on_element=Protractor)
    time.sleep(2.5)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    Appium = driver.find_element(By.XPATH,'/html/body/header/div/div[2]/nav/ul/li[7]/a')
    Appium.click()
    time.sleep(2.5)

    ApachePoi = driver.find_element(By.XPATH,'/html/body/header/div/div[2]/nav/ul/li[8]/a')
    action.click(on_element=ApachePoi)
    time.sleep(2.5)

    Katalon = driver.find_element(By.XPATH,'/html/body/header/div/div[2]/nav/ul/li[9]/a')
    Katalon.click()
    time.sleep(2.5)

    Log4j = driver.find_element(By.XPATH,'/html/body/header/div/div[2]/nav/ul/li[10]/a')
    action.click(on_element=Log4j)
    time.sleep(2.5)

    """Hacemos click en More y luego paseamos con el Chains por sus items sin hacer click"""
    moreItems = driver.find_element(By.XPATH,'/html/body/header/div/div[2]/nav/ul/li[11]/a/span')
    moreItems.click()
    time.sleep(1.5)

    JXL = driver.find_element(By.XPATH,'/html/body/header/div/div[2]/nav/ul/li[11]/ul/li[1]')
    action.move_to_element(JXL).perform()
    time.sleep(1.6)

    ANT = driver.find_element(By.XPATH,'/html/body/header/div/div[2]/nav/ul/li[11]/ul/li[3]')
    action.move_to_element(ANT).perform()
    time.sleep(1.6)

    JTfS = driver.find_element(By.XPATH,'/html/body/header/div/div[2]/nav/ul/li[11]/ul/li[5]')
    action.move_to_element(JTfS).perform()
    time.sleep(1.6)

    FluentAutomation = driver.find_element(By.XPATH,'/html/body/header/div/div[2]/nav/ul/li[11]/ul/li[7]')
    action.move_to_element(FluentAutomation).perform()
    time.sleep(1)

    moreItems = driver.find_element(By.XPATH, '/html/body/header/div/div[2]/nav/ul/li[11]/a/span')
    moreItems.click()

def test_04_search():
    """Nos posicionamos en Barra de Busqueda y tipeamos FIN de Test"""
    search = driver.find_element(By.XPATH,'/html/body/header/div/div[1]/div/section/form/div/div/div[1]/input')
    search.click()
    time.sleep(0.5)

    search.send_keys('FIN de Test')
    time.sleep(1)
    search.clear()
    time.sleep(1)

def test_05_openOtherTab():
    """Abrimos otro tab con la URL de JavaScript Executor"""
    driver.execute_script("window.open('');")
    time.sleep(0.5)

    # change window
    driver.switch_to.window(driver.window_handles[1])
    time.sleep(0.8)

    # Open JavaScript Executor
    driver.get('https://www.seleniumeasy.com/selenium-tutorials/click-element-using-javascriptexecutor')
    assert 'Click element using JavaScriptExecutor | Selenium Easy' in driver.title
    time.sleep(4)

def test_06_dragDrop():
    """Seleccionamos una porcion de texto del bloque de codigo"""
    #Invocamos el Chains
    action = ActionChains(driver)

    #Definimos los puntos de incio (x) y fin (y)
    x = driver.find_element(By.XPATH,'/html/body/div[3]/div/section/article/div[1]/div/div/pre/code/span[13]')
    y = driver.find_element(By.XPATH,'/html/body/div[3]/div/section/article/div[1]/div/div/pre/code/span[21]')
    action.drag_and_drop(x, y).perform()
    time.sleep(2)

@pytest.mark.skip(reason='Marcador de prueba')
def test_07_marcadorPrueba():
    """Probando marcador skip"""
    driver.find_element(By.XPATH,'prueba')
    time.sleep(1)


def test_tearDown():
    """Cerramos el driver"""
    driver.quit()