import os
import re
import requests
import platform
import subprocess
import time as tmp
#from PIL import Image
from colorama import Fore
from pathlib import Path
from selenium import webdriver
from multiprocessing.pool import ThreadPool 
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException,NoSuchElementException,NoSuchWindowException

so = platform.system() 
python = 'python3'if so == 'Linux'else 'python'

def start_http_server(complet):
    if complet == 'frac':
        os.chdir(os.getcwd()+r'/fracmentos')
        subprocess.Popen([f"{python}", "-m", "http.server", "9090"],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
        # print('[+] Corriendo Servidor')

    elif complet == 'comp':
        os.chdir(os.getcwd())
        subprocess.Popen([f"{python}", "-m", "http.server", "9090"],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
        # print('[+] Corriendo Servidor')

def start_ngrok(complet):
    if complet == 'frac':
        os.chdir(os.getcwd()+r'/fracmentos')
        subprocess.Popen(["ngrok", "http", "9090"],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
        # print('[+] Corriendo Tunnel')
    elif complet == 'comp':
        os.chdir(os.getcwd())
        subprocess.Popen(["ngrok", "http", "9090"],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
        # print('[+] Corriendo Tunnel')

class capcha:
    def __init__(self) -> None:
        self.options = None
        self.driver = None
        self.time = None
        self.time_short = None
        self.time_half = None
        self.count = 0
        self.so = platform.system() 
        self.directory = os.getcwd()
        self.complet = self.directory+r'/capcha' if self.so == 'Linux'else self.directory+r'\\capcha'
        self.fracments = self.directory+r'/fracmentos' if self.so == 'Linux'else self.directory+r'\\fracmentos'

    def check_ngrok(self):
        try:
            result = subprocess.run(['ngrok', '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if 'ngrok version' in result.stdout:
                return True, result.stdout.strip()
            else:
                return False, Fore.RED+"[-] Ngrok No Instalada Instalatar Manualmente Desde En https://ngrok.com/"
        except FileNotFoundError:
            return False, Fore.RED+"[-] Ngrok No Instalada Instalatar Manualmente Desde En https://ngrok.com/"

    def base(self):
        if os.path.exists(self.complet):
            if os.path.exists(self.fracments):
                pass
            else:
                os.mkdir(self.fracments)
                print('[+] Creando Directorio Fracments')
        else:
            os.mkdir(self.complet)
            print('[+] Creando Directorio Capcha')
                
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
        # print('[+] Corriendo Servicios')
        # tmp.sleep(5)
        # pool.close()
        # pool.join()

    def search_url_ngrok(self,d1,d2):
        self.service(d1,d2)
        # print('[+] Iniciando Busqueda De Url Ngrok')
        url = 'http://127.0.0.1:4040/inspect/http'
        self.driver.execute_script("window.open('about:blank', 'secondtab');")
        self.driver.switch_to.window("secondtab")
        self.driver.get(url)
        try:
            local = self.time_short.until(EC.presence_of_element_located((By.XPATH,'/html/body/div/div/div/div/div/ul/li/a')))
            url_ngrok = local.get_attribute('href')
            self.driver.close()
            self.driver.switch_to.window(self.driver.window_handles[1])
            # self.driver.close()
            # self.driver.quit() 
            # print(f'[+] Url Ngrok Econtrada: {url_ngrok}')   
            return url_ngrok
        except TimeoutException:
            clear_requests = self.time.until(EC.presence_of_element_located((By.XPATH,'/html/body/div/div/div/div/div/div[2]/div[1]/div/h4/button')))
            clear_requests.click()
            local = self.time.until(EC.presence_of_element_located((By.XPATH,'/html/body/div/div/div/div/div/ul/li/a')))
            url_ngrok = local.get_attribute('href')
            self.driver.close()
            self.driver.switch_to.window(self.driver.window_handles[1])
            # print(f'[+] Url Ngrok Econtrada: {url_ngrok}')   
            return url_ngrok
    
    def Download(self):
        url = 'http://app.sis.gob.pe/SisConsultaEnLinea/Consulta/frmConsultaEnLinea.aspx'
        self.driver.get(url)
        # print("[+] Peticion Get")
        selecccionar = self.time.until(EC.presence_of_element_located((By.ID,'cboTipoBusqueda')))
        select = Select(selecccionar)
        select.select_by_value('1')
        # print("[+] Seleccionando Opcion")

        xpath_capcha = self.time.until(EC.presence_of_element_located((By.XPATH,'/html/body/form/table/tbody/tr[2]/td[2]/div[1]/table/tbody/tr[3]/td/table[3]/tbody/tr[1]/td/div/span[1]/img')))
        url_img = xpath_capcha.get_attribute('src') 
        # print("[+] Buscando Imagen Capcha")

        Download = requests.get(url_img)
        if Download.status_code == 200:
            imagen = Download.content
            nombre_file = 'capcha.jpg'
            try:
                pwd = os.getcwd()+r'/capcha/'+nombre_file 
                with open(pwd,'wb') as archivo:
                    archivo.write(imagen)
                    archivo.close()
            except FileNotFoundError:

                print(Fore.RED+"[-] Archivo No encontrado")
                print(Fore.GREEN+"[+] Creando Directorios")

                os.mkdir(self.complet)
                os.mkdir(self.fracments)

                # print("[+] Captcha Descargado")

    def upload_image_complet(self,fichero):
        define = 'comp'
        url = 'https://www.google.com/search?client=firefox-b-d&q=ll'

        try:
            file = os.listdir(self.complet)[int(fichero)] 
        except FileNotFoundError:
            print(Fore.RED+"[-] Directorio No Encontrado ")

        try:
            self.driver.execute_script("window.open('', 'secondtab');")
            self.driver.switch_to.window("secondtab")

            # *------------------- USO DE GOOGLE LENTS  ------------------------------------------------*
            self.driver.get(url)
            tmp.sleep(6)
            lents = self.driver.find_element(By.CLASS_NAME,'nDcEnd').click()
            tmp.sleep(4)
            # *==========================================================================================*


            # *------------------- TUNEL CREADO CON LA IMAGEN  ------------------------------------------*
            ngrok = self.search_url_ngrok(define,define)
            enlace = self.time.until(EC.presence_of_element_located((By.CSS_SELECTOR,'.cB9M7[jsname="W7hAGe"]')))
            enlace.send_keys(ngrok+r'/capcha/'+file)
            enlace.send_keys(Keys.RETURN)
            # *===========================================================================================*

            # *------------------- CONVERSION DE IMAGEN A TEXTO ------------------------------------------*
            tmp.sleep(4)        
            traducir = self.driver.find_element(By.XPATH,'/html/body/c-wiz/div/div[2]/div/c-wiz/div/div[1]/div/div[3]/div/div/span[3]/span')
            traducir.click()
            tmp.sleep(4)
            cuadro_de_texto = self.time_half.until(EC.presence_of_element_located((By.CLASS_NAME,'QeOavc')))
            texto = cuadro_de_texto.text
            # *============================================================================================*


            # *------------- EVALUACION SI EL TEXTO CUMPLE LA REGLA DE 5 NUMEROS --------------------------*
            solo_numeros = re.sub(r'[^\W\d#,.\n]+', '', texto).strip()
            logitud = len(solo_numeros)
            if int(logitud) == 5:
                print(Fore.GREEN+f'[+] Capcha Resuelto: {texto}')
                self.driver.close()
            else:
                # self.count += 1
                print(f'[+] Capcha No Resuelto: {texto}')
                self.driver.close()
                self.driver.switch_to.window(self.driver.window_handles[0])
                self.driver.refresh()    
                self.Download()

            return logitud,solo_numeros
            # *============================================================================================*

        except TimeoutException:
            self.driver.close()
            self.count += 1
            print(Fore.RED+f"[-] Intento Fallido {self.count}")                
            self.driver.switch_to.window(self.driver.window_handles[0])
            self.driver.refresh()
            self.reset()
            self.Download()

        except NoSuchWindowException:
            self.driver.switch_to.window(self.driver.window_handles[0])
        #     self.driver.refresh()
            # self.reset()
            # self.Download()

        except NoSuchElementException:
            print('[-] No Se Encontro El Elemnto')
            # self.driver.quit()

    def evaluation_response_site_capcha(self):
        # //*[@id="ValidationSummary1"]  expiro
        # //*[@id="ValidationSummary1"] codigo no valido
        try:
            error_capcha = self.time_short.until(EC.presence_of_element_located((By.CSS_SELECTOR,'.cB9M7[jsname="W7hAGe"]')))
            self.count += 1
            print(Fore.RED+f"[-] Intento Fallido {self.count}")                            
        except TimeoutException:
            print(Fore.GREEN+"[+] Capcha verify [✔️  ] ")                            
            
    def formulario_nombres_apellidos(self,capcha):

        Apellido_Paterno = self.time.until(EC.presence_of_element_located((By.ID,'txtPriNombre')))
        Apellido_Paterno.send_keys('tony')        

        Apellido_Paterno = self.time.until(EC.presence_of_element_located((By.ID,'txtSegNombre')))
        Apellido_Paterno.send_keys('ruben')        

        Apellido_Paterno = self.time.until(EC.presence_of_element_located((By.ID,'txtApePaterno')))
        Apellido_Paterno.send_keys('guizado')        

        Apellido_Paterno = self.time.until(EC.presence_of_element_located((By.ID,'txtApeMaterno')))
        Apellido_Paterno.send_keys('vasquez')        

        box_capcha = self.time.until(EC.presence_of_element_located((By.XPATH,'/html/body/form/table/tbody/tr[2]/td[2]/div[1]/table/tbody/tr[3]/td/table[3]/tbody/tr[1]/td/div/span[2]/input')))
        box_capcha.send_keys(capcha)

        Consultar = self.time.until(EC.presence_of_element_located((By.ID,'btnConsultar')))
        Consultar.click()

        self.evaluation_response_site_capcha()

    def run(self):
        instalado, erro = self.check_ngrok()
        if instalado:
            pass
            # print(Fore.GREEN+f"[+] Ngrok Instalada")
        else:
            print(erro)
        

        self.reset()
        print(Fore.GREEN+"[+] Fomateo De Directorios")

        options = Options()
        options.add_argument('--headless')
        self.driver = webdriver.Firefox(options=options)
        self.time = WebDriverWait(self.driver, 60)
        self.time_short = WebDriverWait(self.driver, 5)
        self.time_half = WebDriverWait(self.driver, 5)

        self.Download()
        print(Fore.GREEN+"[+] Captcha Descargado")
        print(Fore.GREEN+'[+] Corriendo Servicios')

        while True:
            try:
                complet,capcha_valor = self.upload_image_complet(0)
                if complet == 5:
                    self.driver.switch_to.window(self.driver.window_handles[0])
                    self.formulario_nombres_apellidos(capcha_valor)
                    tmp.sleep(5)
                    self.driver.quit()
                    break
                else:
                    self.count+=1
                    print(Fore.RED+f"[-] Intento Fallido {self.count}")                
            except TypeError:
                pass
            except KeyboardInterrupt:
                pass
                print(Fore.RED+"[-] Interrupcion del programa ")                
                break
                  
session = capcha()
resolvet = session.run()

# El código registrado no coincide con la imagen mostrada. 
# El código expiró, por favor volver a ingresar el código. 
# buster herramienta que resuelve capcha de audio 