import os
import re
import requests
import subprocess
import time as tmp
from PIL import Image
from pathlib import Path
from selenium import webdriver
from multiprocessing.pool import ThreadPool 
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException,NoSuchElementException

def start_http_server(complet):
    if complet == 'frac':
        os.chdir(r'C:\Users\upset\Documents\programacion\entornos python\capcha_img\fracmentos')
        subprocess.Popen(["python", "-m", "http.server", "9090"],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
        print('[+] Corriendo Servidor')

    elif complet == 'comp':
        os.chdir(r'C:\Users\upset\Documents\programacion\entornos python\capcha_img\capcha')
        subprocess.Popen(["python", "-m", "http.server", "9090"],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
        print('[+] Corriendo Servidor')

def start_ngrok(complet):
    if complet == 'frac':
        os.chdir(r'C:\Users\upset\Documents\programacion\entornos python\capcha_img\fracmentos')
        subprocess.Popen(["ngrok", "http", "9090"],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
        print('[+] Corriendo Tunnel')
    elif complet == 'comp':
        os.chdir(r'C:\Users\upset\Documents\programacion\entornos python\capcha_img\capcha')
        subprocess.Popen(["ngrok", "http", "9090"],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
        print('[+] Corriendo Tunnel')

class capcha:
    def __init__(self) -> None:
        self.options = Options()
        self.driver = webdriver.Firefox(options=self.options)
        self.time = WebDriverWait(self.driver, 60)
        self.directory = os.getcwd()
        self.complet = self.directory+r'\capcha'
        self.fracments = self.directory+r'\fracmentos'

    def reset(self):
        capcha_dir = Path(self.directory) / "capcha"
        fracmentos_dir = Path(self.directory) / "fracmentos"

        if capcha_dir.exists():
            for file in capcha_dir.glob("*"):
                try:
                    os.remove(file)
                except OSError as e:
                    print("Error borrando archivo:", e)
            
        if fracmentos_dir.exists():
            for file in fracmentos_dir.glob("*"):
                try:
                    os.remove(file)
                except OSError as e:
                    print("Error borrando archivo:", e)
            
    def service(self,complet_P,complet_N):
        pool = ThreadPool(2)
        pool.apply_async(start_http_server(complet_P))
        pool.apply_async(start_ngrok(complet_N))
        # tmp.sleep(5)
        # pool.close()
        # pool.join()

    def search_url_ngrok(self,d1,d2):
        self.service(d1,d2)
        print('[+] Iniciando Busqueda De Url Ngrok')
        url = 'http://127.0.0.1:4040/inspect/http'
        self.driver.execute_script("window.open('about:blank', 'secondtab');")
        self.driver.switch_to.window("secondtab")
        self.driver.get(url)
        try:
            local = self.time.until(EC.presence_of_element_located((By.XPATH,'/html/body/div/div/div/div/div/ul/li/a')))
            url_ngrok = local.get_attribute('href')
            self.driver.switch_to.window(self.driver.window_handles[1])
            # self.driver.close()
            # self.driver.quit() 
            print(f'[+] Url Ngrok Econtrada: {url_ngrok}')   
            return url_ngrok
        except TimeoutException:
            clear_requests = self.time.until(EC.presence_of_element_located((By.XPATH,'/html/body/div/div/div/div/div/div[2]/div[1]/div/h4/button')))
            clear_requests.click()
            local = self.time.until(EC.presence_of_element_located((By.XPATH,'/html/body/div/div/div/div/div/ul/li/a')))
            url_ngrok = local.get_attribute('href')
            self.driver.switch_to.window(self.driver.window_handles[1])
            print(f'[+] Url Ngrok Econtrada: {url_ngrok}')   

    
    def upload_image_complet(self):
        define = 'comp'
        # self.service('comp','comp')
        file = os.listdir(self.complet)[0]

        url = 'https://www.google.com/search?client=firefox-b-d&q=ll'

        self.driver.execute_script("window.open('about:blank', 'secondtab');")
        self.driver.switch_to.window("secondtab")
        self.driver.get(url)

        tmp.sleep(4)
        lents = self.driver.find_element(By.CLASS_NAME,'nDcEnd')
        lents.click()
        
        tmp.sleep(4)
        ngrok = self.search_url_ngrok(define,define)
        enlace = self.time.until(EC.presence_of_element_located((By.CSS_SELECTOR,'.cB9M7[jsname="W7hAGe"]')))
        enlace.send_keys(ngrok+file)
        enlace.send_keys(Keys.RETURN)

        tmp.sleep(4)
        # /html/body/c-wiz/div/div[2]/div/c-wiz/div/div[1]/div/div[3]/div/div/span[3]/span/button/span[2]
        traducir = self.driver.find_element(By.XPATH,'/html/body/c-wiz/div/div[2]/div/c-wiz/div/div[1]/div/div[3]/div/div/span[3]/span')
        # traducir = self.time.until(EC.presence_of_element_located((By.XPATH,'/html/body/c-wiz/div/div[2]/div/c-wiz/div/div[1]/div/div[3]/div/div/span[3]/span')))
        # traducir = self.time.until(EC.presence_of_element_located((By.XPATH,'/html/body/c-wiz/div/div[2]/div/c-wiz/div/div[1]/div/div[3]/div/div/span[3]/span/button/span[2]')))
        traducir.click()

        try:
            tmp.sleep(4)
            cuadro_de_texto = self.time.until(EC.presence_of_element_located((By.CLASS_NAME,'QeOavc')))
            texto = cuadro_de_texto.text
            solo_numeros = re.sub(r'\D', '', texto) 
            logitud = len(solo_numeros)
            if int(logitud) == 5:
                print(f'[+] Capcha Resuelto: {texto}')
            else:
                print(f'[+] Capcha No Resuelto: {texto}')
            return logitud,solo_numeros

        except TimeoutException:
            print('[-] No se pudo resolver la imagen')
        
        except NoSuchElementException:
            print('[-] no se encontro el elemnto')
            self.driver.quit()

    def upload_image_fracments(self):
        define = 'frac'
        os.chdir(self.fracments)
        ficheros = os.listdir(os.getcwd())
        
        ngrok = self.search_url_ngrok(define,define)

        longitud = []

        for fichero in ficheros:
            try:
                url = 'https://www.google.com/search?client=firefox-b-d&q=ll'
                
                self.driver.get(url)
                tmp.sleep(4)
                lents = self.driver.find_element(By.CLASS_NAME,'nDcEnd')
                lents.click()
                
                tmp.sleep(4)
                enlace = self.time.until(EC.presence_of_element_located((By.CSS_SELECTOR,'.cB9M7[jsname="W7hAGe"]')))
                enlace.send_keys(ngrok+fichero)
                enlace.send_keys(Keys.RETURN)

                tmp.sleep(4)
                traducir = self.driver.find_element(By.XPATH,'/html/body/c-wiz/div/div[2]/div/c-wiz/div/div[1]/div/div[3]/div/div/span[3]/span')
                # traducir = self.time.until(EC.presence_of_element_located((By.XPATH,'/html/body/c-wiz/div/div[2]/div/c-wiz/div/div[1]/div/div[3]/div/div/span[3]/span')))
                traducir.click()

                try:
                    tmp.sleep(4)
                    cuadro_de_texto = self.time.until(EC.presence_of_element_located((By.CLASS_NAME,'QeOavc')))
                    texto = cuadro_de_texto.text
                    # print(texto)                   
                    longitud.append(texto)
                    
                    solo_numeros = re.sub(r'\D', '', texto) 
                    logitud = len(solo_numeros)
                    if int(logitud) == 5:
                        print(f'[+] Capcha Resuelto: {texto}')
                    else:
                        print(f'[+] Capcha No Resuelto: {texto}')
                except TimeoutException:
                    print('[-] No se pudo resolver la imagen')
                
            except NoSuchElementException:
                print('[-] no se encontro el elemnto')
                self.driver.quit()

        count_longitud = len(longitud)
        print(count_longitud)
        return count_longitud
    
    def fracmentos(self,pwd,output):
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
        print('[+] Fracmentos Separados')

    def formulario_nombres_apellidos(self,capcha):

        Apellido_Paterno = self.time.until(EC.presence_of_element_located((By.ID,'txtPriNombre')))
        Apellido_Paterno.send_keys('tony')        

        Apellido_Paterno = self.time.until(EC.presence_of_element_located((By.ID,'txtSegNombre')))
        Apellido_Paterno.send_keys('ruben')        

        Apellido_Paterno = self.time.until(EC.presence_of_element_located((By.ID,'txtApePaterno')))
        Apellido_Paterno.send_keys('guizado')        

        Apellido_Paterno = self.time.until(EC.presence_of_element_located((By.ID,'txtApeMaterno')))
        Apellido_Paterno.send_keys('vasquez')        

        box_capcha = self.time.until(EC.presence_of_element_located((By.CLASS_NAME,'control')))
        box_capcha.send_keys(capcha)

        Consultar = self.time.until(EC.presence_of_element_located((By.ID,'btnConsultar')))
        Consultar.click()

    def save_img(self):
        self.reset()
        print("[+] Fomateo De Directorios")

        url = 'http://app.sis.gob.pe/SisConsultaEnLinea/Consulta/frmConsultaEnLinea.aspx'
        # options = Options()
        self.options.add_argument('--headless')
        # driver = webdriver.Firefox(options=options)

        self.driver.get(url)
        print("[+] Peticion Get")
        selecccionar = self.time.until(EC.presence_of_element_located((By.ID,'cboTipoBusqueda')))
        select = Select(selecccionar)
        select.select_by_value('1')
        print("[+] Seleccionando Opcion")

        # self.formulario_nombres_apellidos()
        
        xpath_capcha = self.time.until(EC.presence_of_element_located((By.XPATH,'/html/body/form/table/tbody/tr[2]/td[2]/div[1]/table/tbody/tr[3]/td/table[3]/tbody/tr[1]/td/div/span[1]/img')))
        url_img = xpath_capcha.get_attribute('src') 
        print("[+] Buscando Imagen Capcha")

        # self.driver.execute_script("window.open('about:blank', 'secondtab');")
        # self.driver.switch_to.window("secondtab")

        Download = requests.get(url_img)
        if Download.status_code == 200:
            imagen = Download.content
            nombre_file = 'capcha.jpg'
            pwd = os.getcwd()+'\\capcha\\'+nombre_file 
            output = os.path.join(os.getcwd(),'fracmentos')
            with open(pwd,'wb') as archivo:
                archivo.write(imagen)
                archivo.close()
                print("[+] Captcha Descargado")
                self.fracmentos(pwd,output)

                complet,capcha_valor = self.upload_image_complet()
                # fracmentos = self.upload_image_fracments()

                if complet == 5:
                    print('[+] Capcha resuelto con imagen completa')
                    self.driver.switch_to.window(self.driver.window_handles[0])
                    self.formulario_nombres_apellidos(capcha_valor)
                elif complet != 5:
                    print('[+] Iniciando Resolucion De Fracmentos')
                    fracmentos = self.upload_image_fracments()
                #     print('[+] Capcha resuelto con imagen en fracmentos')
                # else:
                #     print("[-] No se pudo descargar el captcha")        
        else:
            print("[-] No se pudo descargar el captcha")

    
session = capcha()
# session.service('comp','comp')
resolvet = session.save_img()
# print(resolvet)








