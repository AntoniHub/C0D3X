from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time

path = Service('Driver/chromedriver.exe')
driver = webdriver.Chrome(service=path)
time.sleep(1)

#Abrimos el Home de Youtube
def test_openWeb():
    driver.get('https://www.youtube.com/')
    driver.maximize_window()
    time.sleep(3)

#Escribimos en la barra la cancion
def test_writeBar():
    bar = driver.find_element(By.XPATH,'/html/body/ytd-app/div[1]/div/ytd-masthead/div[3]/div[2]/ytd-searchbox/form/div[1]/div[1]/input')
    bar.click()
    bar.send_keys('Red Hot Chilli Peppers')
    bar.submit()
    time.sleep(2)

#Seleccionamos cancion como flag para scrollear
def test_selectMusic():
    flag = driver.find_element(By.CLASS_NAME,'ytd-video-renderer')
    driver.execute_script("arguments[0].scrollIntoView();", flag)
    time.sleep(1)
    flag.click()
    time.sleep(5)

#Abrimos otra ventana de Youtube
def test_changeWindow():
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[1])
    driver.get('https://www.youtube.com/')
    time.sleep(2)

#Escribimos cancion
def test_writeMusic2():
    music = driver.find_element(By.XPATH,'/html/body/ytd-app/div[1]/div/ytd-masthead/div[3]/div[2]/ytd-searchbox/form/div[1]/div[1]/input')
    music.click()
    music.send_keys('Queen Champions')
    music.submit()
    time.sleep(2)

#Seleccionamos segunda cancion
def test_selectMusci2():
    queen = driver.find_element(By.CLASS_NAME,'ytd-video-renderer')
    queen.click()
    time.sleep(5)

#Retornamos a la pagina anterior
def test_returnPage():
    driver.switch_to.window(driver.window_handles[0])
    time.sleep(2)
    flag = driver.find_element(By.CLASS_NAME,'ytd-video-renderer')
    driver.execute_script("arguments[0].scrollIntoView();", flag)
    flag.click()
    time.sleep(5)

#Verificamos la anterior
def test_returnAgain():
    driver.switch_to.window(driver.window_handles[1])
    time.sleep(3)

#Cerramos la ventana
def test_closeWeb():
    time.sleep(2)
    driver.quit()