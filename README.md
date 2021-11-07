# autoupdate-webdriver-chrome
This is a tool to auto-update chromedriver by using Python. 

If chromedriver doesn't exist, this program will download the corresponding version of chromedriver and save it in the current folder.

If chromedriver hasn't existed, this program will check the version and update the chrome driver in the current folder.

Although the program is for auto-update chromedriver, you can use the same way of the program as the webdriver to update other browsers.

Using parameter <strong>operatingSystem</strong> to choose win or mac64_m1 or mac64 or linux64

###-----------------------------------------------------------------------------

Using the program, you need to install an extra module - selenium and requests - you can use
```python
pip install -r requirements.txt
```
to install all packages required.

You can run the file directly, you can import it to your Python file too.

If you would like to import to your Python file,

First, download "chromedriver_autoupdate.py" and put it in your working folder, the same folder with your Python file.

Second, using 
```python
from chromedriver_autoupdate import chromedriver_autoupdate
```
at the top of your program.

Third, call method ```check()``` in your program, such as 
```python
chromedriver_autoupdate(operatingSystem = "win").check()
# operatingSystem can be win or mac64_m1 or mac64 or linux64
```

If update chromedriver is successful, it will return ```OK```.

If something is wrong, it will return an error log file name, such as  ```yyyymmdd hhMMss.log```, check detail in a log file.
