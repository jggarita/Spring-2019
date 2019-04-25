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
#pip install prettypandas


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

prdcode=72

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
importcode="China"
importcodeiso="CHN"
#totexporter

for i in range(87,totexporter):
    exporter=i
    mySelect = Select(driver.find_element_by_id("ctl00_c_cboExporter"))
    mySelect.select_by_index(exporter)
    time.sleep(1)
    mySelect = Select(driver.find_element_by_id("ctl00_c_cboExporter"))
    mySelect.select_by_index(exporter)
    selected = mySelect.first_selected_option
    expname=selected.text
    if selected.text==importcode:
        neww=i+1
        time.sleep(3)
        mySelect = Select(driver.find_element_by_id("ctl00_c_cboExporter"))
        mySelect.select_by_index(neww)
        time.sleep(3)
        mySelect = Select(driver.find_element_by_id("ctl00_c_cboImporter"))
        mySelect.select_by_visible_text(importcode)
        time.sleep(2)
    else:
        time.sleep(3)
        mySelect = Select(driver.find_element_by_id("ctl00_c_cboImporter"))
        mySelect.select_by_visible_text(importcode)
        time.sleep(2)
        driver.find_element_by_name("ctl00$c$cmdRunReport").click()
        #Download Table
        time.sleep(15)
        soup_level1=BeautifulSoup(driver.page_source, 'lxml')
        table=soup_level1.find_all('table',class_="box_outline_background")[2]

        #Export to Excel
        
        strings = ['data',str(exporter),'_',importcodeiso,'_',str(prdcode),'.csv']
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


        
        
        



    
   
     


        




