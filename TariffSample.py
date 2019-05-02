    #!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  9 20:04:23 2019

@author: jggarita
"""
#Start from shell

#python
#import selenium
#pip install -U selenium
#pip innstall bs4
#pip install prettypandas
#pip install bs4
#pip install lxml
#Also remember to add path to webdriver.Chrome


## Start
import selenium
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.select import Select
from bs4 import BeautifulSoup


import time
import csv

#######################
#### Lists 

tcount=["Albania", "Armenia", "Cambodia","Nepal", "Russian Federation","Saudi Arabia, Kingdom of","Ukraine","Viet Nam","Yemen"]
isotcount=["ALB","ARM","KHM","NPL","RUS","SAU","UKR","VNM","YEM"]
ntcount=["United States of America","European Union","Brazil","Korea, Republic of","India","South Africa","Costa Rica","Japan","China"]
isontcount=["USA","EUR","BRA","KOR","IND","ZAF","CRI","JPN","CHN"]
prcount=[4,8,17,30,39,61,84,86,87,94]

zcount=tcount+ntcount
isocount=isotcount+isontcount


#tcount=["Albania", "Armenia", "Cambodia","Nepal"] #take 4
#isotcount=["ALB","ARM","KHM","NPL"]
#ntcount=["Brazil","Korea, Republic of","India","South Africa","Costa Rica"] #Take 5 easy
#isontcount=["BRA","KOR","IND","ZAF","CRI"]
#prcount=[4,8,17,30,39,61,85,87,88,95]

#######################
#len(prcount)
for pp in range(4,len(prcount)):
    # Open browser
    driver = webdriver.Chrome()
    driver.get('https://tao.wto.org/welcome.aspx')
    current_url = driver.current_url
    
    ## Login
    username = driver.find_element_by_id('ctl00_c_ctrLogin_UserName')
    username.clear()
    username.send_keys('jgth24@utexas.edu')
    password = driver.find_element_by_id('ctl00_c_ctrLogin_Password')
    password.clear()
    password.send_keys('ZTH24garita')
    driver.find_element_by_name("ctl00$c$ctrLogin$LoginButton").click()
    current_url = driver.current_url
    WebDriverWait(driver, 10).until(EC.url_changes(current_url))
    
    ## Access database
    action = ActionChains(driver)
    firstLevelMenu = driver.find_element_by_id("ctl00_c_rptIDBReports_ctl08_lbReportName")
    firstLevelMenu.click();
    current_url = driver.current_url
    WebDriverWait(driver, 5).until(EC.url_changes(current_url))
    
    ## Select Years (all)
    yearsel=2018
    mySelect = Select(driver.find_element_by_id("ctl00_c_cboStartYear"))
    mySelect.select_by_visible_text(str(yearsel-22))
    time.sleep(1)
    mySelect = Select(driver.find_element_by_id("ctl00_c_cboEndYear"))
    mySelect.select_by_visible_text(str(yearsel))
    selected = mySelect.first_selected_option
    
    ## Select Initial options
    prdcode=prcount[pp]
    mySelect = Select(driver.find_element_by_id("ctl00_c_cboExporter"))
    mySelect.select_by_index(1)
    totexporter=len(mySelect.options)  #Count number of exporters
    
    time.sleep(1)
    mySelect = Select(driver.find_element_by_id("ctl00_c_cboImporter"))
    mySelect.select_by_index(5)
    imponame = mySelect.first_selected_option
    
    time.sleep(1)
    mySelect = Select(driver.find_element_by_id("ctl00_c_cboChapter"))
    mySelect.select_by_index(prdcode)
    
    time.sleep(1)
    radioElement = driver.find_element_by_id("ctl00_c_rbDetail");
    radioElement.click();
    
    time.sleep(2)
    mySelect = Select(driver.find_element_by_id("ctl00_c_cboDetailLevel"))
    mySelect.select_by_index(1)
    
    
    driver.find_element_by_name("ctl00$c$cmdRunReport").click()
    time.sleep(3)
    
    #############################
    # Loop over exporting country
    #############################
    importer=zcount[3] #Armenia
    importcode=isocount[3]
    listbig=["United States of America","China","Japan"]
    for i in range(0,len(zcount)): #start in 0!!!
        exporter=zcount[i]
        mySelect = Select(driver.find_element_by_id("ctl00_c_cboExporter"))
        mySelect.select_by_visible_text(exporter)
        time.sleep(2)
        mySelect = Select(driver.find_element_by_id("ctl00_c_cboExporter"))
        mySelect.select_by_visible_text(exporter)
        selected = mySelect.first_selected_option
        expname=selected.text
        if selected.text==importer:
            neww=i+1
            exportcode=isocount[neww]
            time.sleep(3)
            mySelect = Select(driver.find_element_by_id("ctl00_c_cboExporter"))
            mySelect.select_by_visible_text(zcount[neww])
            time.sleep(3)
            mySelect = Select(driver.find_element_by_id("ctl00_c_cboImporter"))
            mySelect.select_by_visible_text(importer)
            time.sleep(2)
        else:
            exportcode=isocount[i]
            time.sleep(3)
            mySelect = Select(driver.find_element_by_id("ctl00_c_cboImporter"))
            mySelect.select_by_visible_text(importer)
            time.sleep(2)
            driver.find_element_by_name("ctl00$c$cmdRunReport").click()
            #Download Table
            if exporter=="European Union":
                if pp in [6,7,8]:
                    time.sleep(175)
                else:
                    time.sleep(60)
            else:
                if exporter in listbig:
                    if importer in listbig:
                        time.sleep(30)
                    else:
                        time.sleep(20)
                else:
                    if importer in listbig:
                        time.sleep(12)
                    else:
                        time.sleep(10)
    
            soup_level1=BeautifulSoup(driver.page_source, 'lxml')
            table=soup_level1.find_all('table',class_="box_outline_background")[2]
            #Export to Excel
            strings = ['/Users/jggarita/Dropbox/1-RA/PythonWTO/Sample/','data',exportcode,'_',importcode,'_',str(prdcode),'.csv']
            filename=''.join(strings)
            time.sleep(1)
            f=open(filename,'w',newline='')
            writer = csv.writer(f)
            
            tbody=soup_level1('table',class_="box_outline_background")[2].find_all('tr')
            for row in tbody:
                cols=row.findChildren(recursive=False)
                cols=[ele.text.strip() for ele in cols]
                writer.writerow(cols+[expname])
                print(cols)
     
        

        




