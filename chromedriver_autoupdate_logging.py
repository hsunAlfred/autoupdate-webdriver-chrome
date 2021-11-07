from selenium import webdriver
from selenium.common.exceptions import SessionNotCreatedException, WebDriverException
import os
import requests
from zipfile import ZipFile
import traceback
import logging.config
import sys


class chromedriver_autoupdate:
    def __init__(self, operatingSystem):
        self.__errKeyWord = '\nDetail:'
        logging.config.fileConfig('logging.conf')
        self.__logger = logging.getLogger('timeRotateLogger')

        if operatingSystem == "linux64":
            self.__driverZipName = "chromedriver_linux64.zip"
        elif operatingSystem == "mac64":
            self.__driverZipName = "chromedriver_mac64.zip"
        elif operatingSystem == "mac64_m1":
            self.__driverZipName = "chromedriver_mac64_m1.zip"
        elif operatingSystem == "win":
            self.__driverZipName = "chromedriver_win32.zip"
        else:
            print('err:operatingSystem should be win or mac64_m1 or mac64 or linux64, \
                such as \nchromedriver_autoupdate(operatingSystem = "win")')
            sys.exit(1)

    def check(self) -> str:
        '''執行webdriver，檢查chromedriver.exe是否存在另確認版本是否可用'''
        '''建立webdeiver物件，並禁止彈出式視窗'''
        chrome_options = webdriver.ChromeOptions()
        prefs = {"profile.default_content_setting_values.notifications": 2}
        chrome_options.add_experimental_option("prefs", prefs)
        '''背景執行'''
        chrome_options.add_argument("--headless")

        try:
            # print('正在檢查chromedriver元件')
            self.__logger.info(f'正在檢查chromedriver元件')
            driver = webdriver.Chrome(chrome_options=chrome_options)
            driver.quit()
            self.__logger.info(f'OK')
            return 'OK'
        except SessionNotCreatedException as e:
            # print('chromedriver元件版本調整中')
            self.__logger.info(f'chromedriver元件版本調整中')

            f = e.msg.find('Current browser version is') + 27
            t = e.msg.find('with binary path') - 1
            os.remove('chromedriver.exe')

            status = self.__update_driver(e.msg[f:t])
            self.__logger.info(f'{status}')

            if self.__errKeyWord in status:
                return status
            else:
                return self.check()
        except WebDriverException as e:
            # print('chromedriver元件建立中')
            self.__logger.info(f'chromedriver元件建立中')

            status = self.__update_driver('latest')
            self.__logger.info(f'{status}')

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

            driver_url = f'https://chromedriver.storage.googleapis.com/{v}/{self.__driverZipName}'

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
        self.__logger.error(f'{str(e)}\n{traceback.format_exc()}')
        return f'{e}\nDetail: status.log'


if __name__ == '__main__':
    print(chromedriver_autoupdate(operatingSystem="win").check())
    input('press enter to exit')
