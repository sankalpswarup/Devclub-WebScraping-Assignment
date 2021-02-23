from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
# choosing to run chrome in headless mode
options=webdriver.ChromeOptions()
options.headless=False

PATH="D:\DevClub\Web Scraping Assignment\chromedriver.exe"
driver = webdriver.Chrome(PATH,options=options)

driver.get("https://codeforces.com/problemset")
round=input("Please enter the round number : ")
os.mkdir(str(round))
val=65
try: 
    while driver.find_element_by_link_text(str(round)+chr(val)).is_displayed() :
        # making folder of each problem
        os.mkdir(f"./{str(round)}/{chr(val)}")
        # going to each problem
        driver.find_element_by_link_text(str(round)+chr(val)).send_keys(Keys.RETURN)
        test = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME,"problem-statement"))
        )
        # setting windows size to capture whole window
        S= lambda X: driver.execute_script('return document.body.parentNode.scroll'+X)
        driver.set_window_size(S('Width'),S('Height'))
        # finding element and taking screenshot
        problem=driver.find_element_by_class_name("problem-statement")
        problem.screenshot(f"./{str(round)}/{chr(val)}/problem.png")
        
        # writing input and output to text files
        examples=driver.find_elements_by_tag_name("pre")
        i=1
        for example in examples :
            if(i%2!=0):
                text_file=open("./"+str(round)+"/"+chr(val)+"/Input "+str((i+1)/2)+".txt","w")
                text_file.write(example.text)
                text_file.close()
            else:
                text_file=open("./"+str(round)+"/"+chr(val)+"/Output "+str(i/2)+".txt","w")
                text_file.write(example.text)
                text_file.close()
            i=i+1
        # goind back to problems page
        driver.back()
        test = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME,"problems"))
        )

        # increasing val for next problem
        val=val+1

finally:
    driver.quit()
