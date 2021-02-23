from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os

# this function returns the index from which the problem tag starts, ie A,B,C1,C2,etx
def check(text):
    ind=0
    found=False
    while(not(found)):
        val=ord(text[ind])
        if(val>=48 and val<=57):
            ind+=1
        else:
            found=True
    return ind

round=input("Please enter the round number : ")

# choosing to run chrome in headless mode
options=webdriver.ChromeOptions()
options.headless=True

PATH="D:\DevClub\Web Scraping Assignment\chromedriver.exe"
driver = webdriver.Chrome(PATH,options=options)

driver.get("https://codeforces.com/problemset")

os.mkdir(str(round))
found=False
run=True
# run tells whether the while loop will run or not
# found tells whether the matching round is found or not
try:
    while run :
        if(found):  
             run=False

        prob_label=driver.find_elements_by_partial_link_text(str(round))
        # if matching round is not found on the current page
        if((not prob_label)):
            # list is empty
            # opening next page
            driver.find_element_by_link_text("→").send_keys(Keys.RETURN)
            test = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME,"problems"))
            )
            continue
            # it will now check for next page
        else:
            # list is not empty
            found=True

        string=prob_label[0].text
        char=string[len(str(round))]

        # the following lines of code are used to remove undesired cases selected by find_element_by_partial_link_text
        # example, for round 147, round 1470 will also be selected but that is not desired
        # it checks whether the round selected completely matches with the entered round
        # it does so by checking the position of first alphabet after the round number
        if(ord(char)>=48 and ord(char)<=57):
            is_digit=True
        else:
            is_digit=False

        if(is_digit):
            # wrong case matched
            found=False
            continue

        # storing each problem label in a new list
        label_list=[]
        for x in prob_label :
            label_list.append(x.text)
        
        for label in label_list:
            # referencing each problem link page by using its link text
            element=driver.find_element_by_link_text(label)
            index=check(label)
            # making folder of each problem
            os.mkdir(str(round)+"/"+label[index:])
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
            problem.screenshot(f"./{str(round)}/{label[index:]}/problem.png")
            
            # writing input and output to text files
            examples=driver.find_elements_by_tag_name("pre")
            i=1
            for example in examples :
                if(i%2!=0):
                    text_file=open("./"+str(round)+"/"+label[index:]+"/Input "+str((i+1)/2)+".txt","w")
                    text_file.write(example.text)
                    text_file.close()
                else:
                    text_file=open("./"+str(round)+"/"+label[index:]+"/Output "+str(i/2)+".txt","w")
                    text_file.write(example.text)
                    text_file.close()
                i=i+1
            # going back to problems page
            driver.back()
            test = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME,"problems"))
            )
        if(run):
            # this is used to change one more page after the matching case is found
            # to incorporate problems of the mathcing case on next page (if they are there)
            driver.find_element_by_link_text("→").send_keys(Keys.RETURN)
            test = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME,"problems"))
            )

     
finally:
    driver.quit()



