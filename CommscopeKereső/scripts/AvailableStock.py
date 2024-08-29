from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep

from pathlib import Path
from glob import glob
from pandas import read_excel
import os

import mysql.connector
from datetime import date

try:
    #Opening browser
    driver = webdriver.Edge()

    #Setting wait times
    short_wait = WebDriverWait(driver, 15)
    long_wait = WebDriverWait(driver, 60)

    #Opening the link
    driver.get("https://availablestock.commscope.com/PartNumberList.aspx")

    #Logging in if needed
    username_input = short_wait.until(EC.visibility_of_element_located((By.ID, "signInName")))

    if username_input:
        username_input.send_keys("melovics@omikron.hu")

        next_button = short_wait.until(EC.visibility_of_element_located((By.ID, "next")))
        next_button.click()

        password_input = long_wait.until(EC.visibility_of_element_located((By.ID, "password")))
        password_input.send_keys("Madzag12")

        next_button = long_wait.until(EC.visibility_of_element_located((By.ID, "next")))
        next_button.click()

    #Downloading excel sheet
    save_button = long_wait.until(EC.visibility_of_element_located((By.ID, "phBody_btnExportExcel")))
    save_button.click()

    sleep(10) #Waiting for the download to finish

    #Closing browser
    driver.quit()

    #Reading last downloaded xlsx
    files = glob(str(Path.home())+"\\Downloads\\AvailableStock*.xlsx")
    latest = max(files, key=os.path.getmtime)
    table = read_excel(latest).values.tolist()
    os.remove(latest)

    #SQL
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="commscopelocal"
    )

    cursor = db.cursor()

    datum = date.today().strftime("%Y-%m-%d")
    sql = "REPLACE INTO KESZLET (cikkszam, raktar, mennyiseg, mertekegyseg, lekerve) VALUES "
    for line in table:
        #raktár megnevezés feldolgozása
        temp1 = line[2].split("(")
        temp2 = temp1[0].split("-")
        temp3 = temp1[1].split(")")
        orszag = temp2[0].strip()
        azon   = temp3[0].strip()
        if len(temp2) >= 2:
            varos = temp2[1].strip()
        else: 
            varos = temp2[0].strip()
        #mennyiség és mértékegység szétválasztása
        temp1 = line[-1].split(" ")
        mennyiseg = temp1[0]
        mertekegyseg = temp1[1]
        #raktár ellenőrzése és esetileg felvitele
        cursor.execute(f"SELECT azon FROM RAKTARAK WHERE azon LIKE '{azon}'")
        if len(cursor.fetchall()) < 1:
            cursor.execute(f"INSERT INTO RAKTARAK (azon, varos, orszag) VALUES ('{azon}','{varos}','{orszag}')")
        #készlet felvitele
        sql += f"('{line[0]}','{azon}','{mennyiseg}','{mertekegyseg}', '{datum}'),"
    sql = sql[0:-1] #utolsó vessző kitörlése

    cursor.execute(sql)
    db.commit()

except Exception as e:
    print("\nHiba a raktárkészlet lekérése/mentése közben:",e,"\n\n")