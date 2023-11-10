from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.support.select import Select
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
from PIL import Image
import time as tmp 
import os

def reset():
    pwd = r'C:\Users\upset\Documents\programacion\entornos python\capcha_img'
    capcha = r'\capcha'
    fracmentos = r'\fracmentos'

    os.chdir(pwd+f'{capcha}')
    os.system('del *.jpg')

    os.chdir(pwd+f'{fracmentos}')
    os.system('del *.jpg')

def reconocimiento():
    url = 'https://www.google.com/search?client=firefox-b-d&q=ll'
    # options = Options()
    # options.add_argument('--headless')
    driver = webdriver.Firefox()
    driver.get(url)
    time = WebDriverWait(driver, 60)
    # lents = time.until(EC.presence_of_element_located((By.CSS_SELECTOR,'div[jsname="R5mgy"]')))
    lents = time.until(EC.presence_of_element_located((By.CLASS_NAME,'nDcEnd')))
    lents.click()

    image_backgroud = time.until(EC.presence_of_element_located((By.CSS_SELECTOR,'div.f6GA0')))
    actions = ActionChains(driver)
    actions.drag_and_drop('', image_backgroud)
    actions.perform()

def fracments(pwd,output):
    filename = os.path.basename(pwd)

    img = Image.open(pwd)

    name, ext = os.path.splitext(filename)

    # Obtener el ancho y alto de la imagen
    width, height = img.size

    # Calcular el ancho de cada parte recortada
    crop_width = width // 5

    # Recorrer las 5 partes
    for i in range(5):

        # Calcular las coordenadas del recorte
        left = i * crop_width
        top = 0   
        right = (i+1) * crop_width
        bottom = height

        # Hacer el recorte
        cropped = img.crop((left, top, right, bottom))

        # Guardar la imagen recortada
        crop_name = f"{name}_parte{i+1}{ext}"
        crop_path = os.path.join(output, crop_name)

        cropped.save(crop_path)

    print('** fracmentos separados')

        # Mostrar la imagen recortada
        # cropped.show()

def save_img():
    url = 'http://app.sis.gob.pe/SisConsultaEnLinea/Consulta/frmConsultaEnLinea.aspx'
    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Firefox(options=options)

    driver.get(url)
    time = WebDriverWait(driver, 60)

    # op = input(str('1)Datos Personales\n2)Tipo de Documento'))

    selecccionar = time.until(EC.presence_of_element_located((By.ID,'cboTipoBusqueda')))
    select = Select(selecccionar)
    select.select_by_value('1')

    xpath_capcha = time.until(EC.presence_of_element_located((By.XPATH,'/html/body/form/table/tbody/tr[2]/td[2]/div[1]/table/tbody/tr[3]/td/table[3]/tbody/tr[1]/td/div/span[1]/img')))
    url_img = xpath_capcha.get_attribute('src') 

    Download = requests.get(url_img)
    if Download.status_code == 200:
        imagen = Download.content
        nombre_file = 'capcha.jpg'
        pwd = os.getcwd()+'\\capcha\\'+nombre_file 
        output = os.path.join(os.getcwd(),'fracmentos')

        with open(pwd,'wb') as archivo:
            archivo.write(imagen)
            archivo.close()
            print("** Captcha descargado")
            fracments(pwd,output)
            
    else:
        print("No se pudo descargar el captcha")



    # /html/body/form/table/tbody/tr[2]/td[2]/div[1]/table/tbody/tr[3]/td/table[3]/tbody/tr[1]/td/div/span[1]/img

# http://app.sis.gob.pe/SisConsultaEnLinea/Consulta/frmConsultaEnLinea.aspx
# http://app.sis.gob.pe/SisConsultaEnLinea/Consulta/CaptchaImage.aspx?guid=6d49618d-a282-44a3-bd4e-a3102f781fa2
# CaptchaImage.aspx?guid=6d49618d-a282-44a3-bd4e-a3102f781fa2

# convertir png a jpg si se cambia la extension
# manualmente no lo leeera 
# se necesita que se convierta a jpg de manera 
# online sino produce una url
# solo se puede cortar en formato jpg

# guardar la imagen y convertirla de png a jpg 
# recotar la imagen en 5 fracmentos 
# subir un fotograma y usarlo en google lents
# si me devuele menos de 5 digitos 
# ver que numero que se subio no se puede resolver 
# con google lents
# https://lens.google.com/search?ep=gsbubb&hl=es-419&re=df&p=AbrfA8pGZ00WKHM6Kq41nhOoWkx4K4G0Nn-1kBR5uIfY0F93c45bOrBHewrOHZh68u2q8t5-IgddZWKCK7SQdl2qopPF3gRcZ3dnxkJknN72t_SaAziT8VJjC-y8hFlEYFhmYFpVRm80ZlKhqYp59pKMpi1cQex0F42CirNebeNvLIaLfdaB3gH_-m_Anv7H3ONOUHpPOT8P-rPBn7UJk30%3D#lns=W251bGwsbnVsbCxudWxsLG51bGwsbnVsbCxudWxsLG51bGwsIkVrY0tKRE15TXpjek16RTRMV1JoTVRNdE5HWTVaUzA1Wmpoa0xXUXdNREE0Wm1WallUTTNaaElmT0RZMFUwbE9UakZxWnpSVmMwZEZNRGhCY0VaUVRsOWlhVTB0YTNWNFp3PT0iLG51bGwsbnVsbCxudWxsLDMsWyJhdXRvIiwiZXMiXSxbW11dXQ==

save_img()
# reconocimiento()
# reset()
# pwd = r'C:\Users\upset\Documents\programacion\entornos python\capcha_img\capcha\capcha.jpg'
# output = r'C:\Users\upset\Documents\programacion\entornos python\capcha_img\fracmentos'
# fracments(pwd,output)
