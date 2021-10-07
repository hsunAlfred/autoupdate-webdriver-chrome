from selenium import webdriver
from selenium.common.exceptions import SessionNotCreatedException, WebDriverException
import os
import requests
from zipfile import ZipFile
import traceback
from datetime import datetime

class chromedriver_autoupdate:
    def __init__(self):
        pass

    def check(self) -> str:
        '''執行webdriver，檢查chromedriver.exe是否存在另確認版本是否可用'''
        '''建立webdeiver物件，並禁止彈出式視窗'''
        chrome_options = webdriver.ChromeOptions()
        prefs = {"profile.default_content_setting_values.notifications":2}
        chrome_options.add_experimental_option("prefs",prefs)
        '''背景執行'''
        chrome_options.add_argument("--headless")

        try:
            print('正在檢查chromedriver元件')
            driver = webdriver.Chrome(chrome_options=chrome_options)
            driver.quit()
            return 'OK'
        except SessionNotCreatedException as e:
            print('chromedriver元件版本調整中')
            f = e.msg.find('Current browser version is') + 27
            t = e.msg.find('with binary path') - 1
            os.remove('chromedriver.exe')
            status = self.__update_driver(e.msg[f:t])
            if 'ERROR' in status:
                return status
            else:
                return self.check()
        except WebDriverException as e:
            print('chromedriver元件建立中')
            status = self.__update_driver('latest')
            if 'ERROR' in status:
                return status
            else:
                return self.check()
        except:
            log_file_name = f'{time_get()}.log'
            with open(log_file_name, 'a', encoding='UTF-8') as f:
                traceback.print_exc(file = f)
            return f'ERROR {log_file_name}'
        
    def __update_driver(self, version):

        url = 'https://chromedriver.chromium.org/downloads'
        v = 0

        try:
            re = requests.get(url).text
        except:
            d = datetime.now()
            mm = d.month if d.month >= 10 else '0' + str(d.month)
            dd = d.day if d.day >= 10 else '0' + str(d.day)
            hh = d.hour if d.hour >= 10 else '0' + str(d.hour)
            mi = d.minute if d.minute >= 10 else '0' + str(d.minute)
            ss = d.second if d.second >= 10 else '0' + str(d.second)
            log_file_name = f'{d.year}{mm}{dd}_{hh}{mi}{ss}.log'
            with open(log_file_name, 'a', encoding='UTF-8') as f:
                traceback.print_exc(file = f)
            return f'ERROR {log_file_name}'
        else:
            if version == 'latest':
                temp = re.find('If you are using Chrome version')
                v = re[temp:temp+100].split('\n')[0].split(' ')[-1]
            else:
                temp_end = re.find(f'Supports Chrome version {version.split(".")[0]}')
                temp_start = re[:temp_end].rfind('ChromeDriver')
                v = re[temp_start:temp_end].split('</strong>')[0].split(' ')[1]
            
            driver_url = f'https://chromedriver.storage.googleapis.com/{v}/chromedriver_win32.zip'
            ref = requests.get(driver_url)

            download_file = 'driver.zip'
            with open(download_file, 'wb') as f:
                f.write(ref.content)
            ZipFile(download_file, 'r').extractall()
            os.remove(download_file)
        
        return 'OK'

def time_get():
    d = datetime.now()  
    mm = d.month if d.month >= 10 else '0' + str(d.month)
    dd = d.day if d.day >= 10 else '0' + str(d.day)
    hh = d.hour if d.hour >= 10 else '0' + str(d.hour)
    mi = d.minute if d.minute >= 10 else '0' + str(d.minute)
    ss = d.second if d.second >= 10 else '0' + str(d.second)

    return f'{d.year}{mm}{dd}_{hh}{mi}{ss}'


if __name__ == '__main__':
    print(chromedriver_autoupdate().check())
    input('press enter to exit')