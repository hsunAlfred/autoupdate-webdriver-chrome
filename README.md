# autoupdate-webdriver-chrome
This is a tool to autoupdate chromedriver by using Python. 

If chromedriver doesn't exist, this program will download the correspond version of chromedriver and save in the current folder.

If chromedriver hasn't exist, this program will check the version and update the chrome driver in the current folder.

Although the program is for autoupdate chromedriver, you can use the same way of the program like the webdriver to update other brower.

Because I only use chromedriver, the program can only for chromedriver.XDD

###-----------------------------------------------------------------------------

Using the program, you need to install extral modual - selenium and requests - 
```python
pip install -r requirements.txt
```
.

You can run the file directly, you can import to your Python file too.

If you would like to import to your Python file,

First, download "chromedriver_autoupdate.py" and put it in you working folder, the same folder with you Python file.

Second, using 
```python
from chromedriver_autoupdate import chromedriver_autoupdate
```
in the top of your program, .

Third, call method ```check()``` in your program, sucj as 
```python
chromedriver_autoupdate().check()
```

If update chromedriver successful, it will return ```OK```.

If somethin wrong, it will return error log file name, such as  ```yyyymmdd hhMMss.log```, check detail in log file.
