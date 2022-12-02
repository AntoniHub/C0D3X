from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time
import selenium

path = Service('Driver/chromedriver.exe')
driver = webdriver.Chrome(service=path)
time.sleep(0.5)

#Abrimos el navegador con la URL
def test_openWeb():
    driver.get('https://www.amazon.com/-/es/')
    driver.maximize_window()
    time.sleep(1.5)

#Hacemos click en la configuracion
def test_clickSetting():
    all = driver.find_element(By.XPATH,'/html/body/div[1]/header/div/div[4]/div[1]/a/i')
    all.click()
    time.sleep(1)

#Scrolleamos hasta ver all
def test_scrollSeeAll():
    seeAll = driver.find_element(By.XPATH,'/html/body/div[4]/div[2]/div/ul[1]/ul[2]/li[2]/a')
    driver.execute_script("arguments[0].scrollIntoView();", seeAll)
    time.sleep(1.5)
    seeAll.click()
    time.sleep(1)


#Clickeamos ver menos
def test_seeLess():
    seeLess = driver.find_element(By.XPATH,'/html/body/div[4]/div[2]/div/ul[1]/li[18]/a[2]')
    seeLess.click()
    time.sleep(1)

#Subimos a ELECTRONICOS
def test_electronics():
    select = driver.find_element(By.XPATH,'/html/body/div[3]/div[2]/div/ul[1]/li[7]/a/i')
    driver.execute_script("arguments[0].scrollIntoView();", select)
    time.sleep(1.5)
    select.click()
    time.sleep(1)

#Seleccionamos telefonia
def test_phone():
    phone = driver.find_element(By.XPATH,'/html/body/div[3]/div[2]/div/ul[5]/li[6]/a')
    phone.click()
    time.sleep(2)

#Abrimos el comboBox
def test_comboBox():
    combo = driver.find_element(By.XPATH,'/html/body/div[1]/header/div/div[1]/div[2]/div/form/div[2]/div/div/select')
    combo.click()
    time.sleep(1)
    combo.click()
    time.sleep(1)

#Buscamos iPhone
def test_findIphone():
    iphone = driver.find_element(By.ID,'twotabsearchtextbox')
    iphone.click()
    time.sleep(0.5)
    iphone.send_keys('iPhone 13 PRO MAX')
    iphone.submit()
    time.sleep(1)

#CERRAMOS!
def test_close():
    time.sleep(2)
    driver.quit()