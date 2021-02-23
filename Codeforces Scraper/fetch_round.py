from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
# choosing to run chrome in headless mode
options=webdriver.ChromeOptions()
options.headless=True

PATH="D:\DevClub\Web Scraping Assignment\chromedriver.exe"
driver = webdriver.Chrome(PATH,options=options)

driver.get("https://codeforces.com/problemset")
round=input("Please enter the round number : ")

os.mkdir(str(round))
prob_label=driver.find_elements_by_partial_link_text(str(round))
# storing each problem label in a new list
label_list=[]
for x in prob_label :
    label_list.append(x.text)

try:
    for label in label_list:
        # referencing each problem link page by using its link text
        element=driver.find_element_by_link_text(label)

        # making folder of each problem
        os.mkdir(str(round)+"/"+label[4:])
        # going to each problem
        element.send_keys(Keys.RETURN)
        test = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME,"problem-statement"))
        )
        # setting windows size to capture whole window
        S= lambda X: driver.execute_script('return document.body.parentNode.scroll'+X)
        driver.set_window_size(S('Width'),S('Height'))
        # finding element and taking screenshot
        problem=driver.find_element_by_class_name("problem-statement")
        problem.screenshot(f"./{str(round)}/{label[4:]}/problem.png")
        
        # writing input and output to text files
        examples=driver.find_elements_by_tag_name("pre")
        i=1
        for example in examples :
            if(i%2!=0):
                text_file=open("./"+str(round)+"/"+label[4:]+"/Input "+str((i+1)/2)+".txt","w")
                text_file.write(example.text)
                text_file.close()
            else:
                text_file=open("./"+str(round)+"/"+label[4:]+"/Output "+str(i/2)+".txt","w")
                text_file.write(example.text)
                text_file.close()
            i=i+1
        # going back to problems page
        driver.back()
        test = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME,"problems"))

        )

     
finally:
    driver.quit()
