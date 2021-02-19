from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

PATH="D:\DevClub\Web Scraping Assignment\chromedriver.exe"
driver = webdriver.Chrome(PATH)

driver.get("https://moodle.iitd.ac.in/login/index.php")

uname = driver.find_element_by_id("username")
username=input("Pls enter your username:")
uname.send_keys(username)
pword = driver.find_element_by_id("password")
password=input("Pls enter your Password:")
pword.send_keys(password)

text = driver.find_element_by_id("login").text

l=text.splitlines()
captcha=l[3]
if(captcha.find("add")!=-1):
    index=captcha.find("add")
    num1=captcha[index+4:index+6]
    num2=captcha[index+9:index+11]
    ans=int(num1)+int(num2)
    


elif(captcha.find("subtract")!=-1):

    index=captcha.find("subtract")
    num1=captcha[index+9:index+11]
    num2=captcha[index+14:index+16]
    ans=int(num1)-int(num2)
    

elif(captcha.find("first value")!=-1):

    index=captcha.find("first value")
    num1=captcha[index+12:index+14]
    num2=captcha[index+17:index+19]
    ans=int(num1)
    

else:

    index=captcha.find("second value")
    num1=captcha[index+13:index+15]
    num2=captcha[index+18:index+20]
    ans=int(num2)


field=driver.find_element_by_id("valuepkg3")
field.clear()
field.send_keys(ans)


login = driver.find_element_by_id("loginbtn")
login.send_keys(Keys.RETURN)



