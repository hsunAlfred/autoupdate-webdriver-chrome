from selenium import webdriver
from selenium.common.exceptions import SessionNotCreatedException, WebDriverException
import os
import requests
from zipfile import ZipFile
import traceback
from datetime import datetime


class chromedriver_autoupdate:
    def __init__(self):
        self.__errKeyWord = '\nDetail:'

    def check(self) -> str:
        '''執行webdriver，檢查chromedriver.exe是否存在另確認版本是否可用'''
        '''建立webdeiver物件，並禁止彈出式視窗'''
        chrome_options = webdriver.ChromeOptions()
        prefs = {"profile.default_content_setting_values.notifications": 2}
        chrome_options.add_experimental_option("prefs", prefs)
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
            if self.__errKeyWord in status:
                return status
            else:
                return self.check()
        except WebDriverException as e:
            print('chromedriver元件建立中')
            status = self.__update_driver('latest')
            if self.__errKeyWord in status:
                return status
            else:
                return self.check()
        except Exception as e:
            return self.__errLog(e)

    def __update_driver(self, version):

        url = 'https://chromedriver.chromium.org/downloads'
        v = 0

        try:
            re = requests.get(url).text
        except Exception as e:
            return self.__errLog(e)
        else:
            if version == 'latest':
                temp = re.find('If you are using Chrome version')
                v = re[temp:temp+100].split('\n')[0].split(' ')[-1]
            else:
                temp_end = re.find(
                    f'Supports Chrome version {version.split(".")[0]}')
                temp_start = re[:temp_end].rfind('ChromeDriver')
                v = re[temp_start:temp_end].split('</strong>')[0].split(' ')[1]

            driver_url = f'https://chromedriver.storage.googleapis.com/{v}/chromedriver_win32.zip'
            print(driver_url)
            try:
                ref = requests.get(driver_url)
            except Exception as e:
                return self.__errLog(e)

            download_file = 'driver.zip'
            with open(download_file, 'wb') as f:
                f.write(ref.content)
            ZipFile(download_file, 'r').extractall()
            os.remove(download_file)

        return 'OK'

    def __errLog(self, e):
        log_file_name = f'{datetime.now().strftime("%Y-%m-%d %H_%M_%S")}.log'
        with open(log_file_name, 'a', encoding='UTF-8') as f:
            traceback.print_exc(file=f)
        return f'{e}\nDetail: {log_file_name}'


if __name__ == '__main__':
    print(chromedriver_autoupdate().check())
    input('press enter to exit')
