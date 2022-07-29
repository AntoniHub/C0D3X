import time
from behave import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains


"""
Deshabilitar JS
opt.add_argument('--disable-javascript')
opt.add_experimental_option("prefs",{'profile.managed_default_content_settings.javascript': 2})
"""
opt = Options()
#Maximizamos la ventana desde que se inicia la ejecucion
opt.add_argument('--start-maximized')
#Quitamos el aviso de que el navegador es cotrolado por otro Software
opt.add_experimental_option("excludeSwitches", ["enable-automation"])
opt.add_experimental_option('useAutomationExtension', False)

"""
    Comenzamos a utilizar 

    Cucumber en Python 
    
    (Behave)
"""

@given('Launch chrome browser')
def launchBrowser(context):
    #Inicializamos WebDriver
    context.driver = webdriver.Chrome(chrome_options=opt, executable_path='Driver/chromedriver.exe')
    time.sleep(0.5)

    #Abrimos la pagina de ESPN
    context.driver.get('https://www.espn.com.ar/')
    context.driver.maximize_window()
    time.sleep(8)
    #context.driver.switch_to.frame('google_ads_iframe_/21783347309/espn.latam.ar/frontpage/index_1')
    #context.driver.switch_to.default_content()

@when('View ESPN HomePage')
def viewPage(context):
    #Visualizamos seccion de Futbol
    context.action = ActionChains(context.driver)
    context.fut = context.driver.find_element(By.XPATH, '/html/body/div[5]/div[2]/header/nav[1]/ul/li[1]/a/span/span[1]')
    context.action.move_to_element(context.fut).click().perform()
    time.sleep(2)

    #Visualizamos seccion de Rugby
    context.rgb = context.driver.find_element(By.XPATH,'/html/body/div[5]/div[2]/header/nav[1]/ul/li[2]/a/span/span[1]')
    context.action.move_to_element(context.rgb).click().perform()
    time.sleep(2)

    #Visualizamos seccion de Tenis
    context.tns = context.driver.find_element(By.XPATH,'/html/body/div[5]/div[2]/header/nav[1]/ul/li[3]/a/span/span[1]')
    context.action.move_to_element(context.tns).click().perform()
    time.sleep(2)

    #Visualizamos seccion de Basket
    context.bsk = context.driver.find_element(By.XPATH,'/html/body/div[5]/div[2]/header/nav[1]/ul/li[4]/a/span/span[1]')
    context.action.move_to_element(context.bsk).click().perform()
    time.sleep(2)

    #Visualizamos seccion de F1
    context.f1 = context.driver.find_element(By.XPATH,'/html/body/div[5]/div[2]/header/nav[1]/ul/li[5]/a/span/span[1]')
    context.action.move_to_element(context.f1).click().perform()
    time.sleep(2)

    #Visualizamos seccion de Hockey
    context.hcky = context.driver.find_element(By.XPATH,'/html/body/div[5]/div[2]/header/nav[1]/ul/li[6]/a/span/span[1]')
    context.action.move_to_element(context.hcky).click().perform()
    time.sleep(2)

    #Visualizamos mas secciones
    context.more = context.driver.find_element(By.XPATH,'/html/body/div[5]/div[2]/header/nav[1]/ul/li[7]/div/ul')
    context.action.move_to_element(context.more).click().perform()
    time.sleep(2)

@then('Quick view to page')
def scrollPage(context):
    """
    Scrolleamos hasta el final de la pagina utilizando la seccion NFL
    como flag para ejecutar codigo JavaScript en Python
    """
    context.nfl = context.driver.find_element(By.CLASS_NAME,'quicklinks_list__name')
    context.driver.execute_script("arguments[0].scrollIntoView();", context.nfl)
    time.sleep(2.5)

@then('Close browser')
def closeBrowser(context):
    #Cerramos la ventana
    context.driver.close()