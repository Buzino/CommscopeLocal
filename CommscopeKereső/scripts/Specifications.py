from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from pyautogui import hotkey, typewrite, press
import pyperclip
from pathlib import Path
from glob import glob
import os

def waitabit():
    sleep(1.5)

#Opening browser
driver = webdriver.Edge()

#Defining wait times
wait_common = WebDriverWait(driver,5)

#Opening the link
driver.get("https://www.commscope.com/")

#Closing cookies tab
try:
    WebDriverWait(driver,3).until(EC.visibility_of_element_located((By.CLASS_NAME, "onetrust-close-btn-ui"))).click()
except:
    pass

#Queries
queries = ['884036134/32','884055854/16','884028704/10','4-2153161-1','760241185','884019038/32','760242571','810010011/DB','884026514/10','185705-1','1-2843018-1','700206667','700206725','1-2153365-3','760092429','2153449-4','760252172','2160855-1','760255469','760004184','760081265','760240201','1427278-3','760244968','760106062','760242503','884015704/10','901-R350-WW02','737891-2','810010169/DB','LSA-7014A250-00','1375191-2','57535-2','760081323','760237884','810009649/DB','760154971','884023938/32','64685043-10','CC8459744/BU','760077800','884050654/16','760077826','760107334','884016204/10','EC6477-000','1-1375055-3','336348-2','2153449-2','8107990/DB','760154963','884064854/16','760243525','760249273','2160032-2','1427071-2','1711008-1']
queries = ['9U1-R350-WW03','760246345','ICX7150-48PF-4RA','902-1170-AR00','60891121-06','NPC6ASZDB-YL001M','CV7092-000','1711732-3','E25G-SFP-TWX-P-51','760072959','740-64310-001','ICX7750-26Q','860644155','760246288','HST-B8HNA0150NN000','CPCSSZ2-06F025','740-64112-110','760245679','FGS-MH4E-H','ICX7000-C12-WMK','CA111K2-03F010','902-0173-AU00','760036293','ICX8200-48PF2-E2','ICX7150-C12P-2X10R','760230938','65772812-02','CC6325-000','BTM002-M14.0','760242750']
queries = ['760159988','1499101-1','NPC6ASZDB-WT002M','1711163-1','884016558/99','9-1711163-1','NPC6ASZDB-WT001M','3-57893-1','760248525','219106-1','57893-2','700216450','760243331','2153449-4','760243327','884032314/10','1-219106-7','6-641335-2','1-219106-5','NPC6ASZDB-WT005M','FFWLCLC42-JXF004','NCC44SZDB-08M015','NPC06UZDB-WT002M','1-1116412-3','2153449-2','2-599625-4','57535-2','NPC6ASZDB-WT003M','NPC6ASZDB-WT150C','1-6457567-6','1933286-4','760184820','NCC44SZDB-08M010','108232745','1-1933671-3','1375055-2','1-6536501-0','1671000-8','1671281-1','1671495-2','1671495-6','1673956-1.','1711797-1','1725150-3.','1725150-6.','2153437-1','2160046-5','2269081-4','2-336613-1','2843021-3','2-964830-1','2-966224-1','2-966740-1','5-336608-1','6-2843007-1','6536501-1','6536501-2','6536501-3','6536501-5','6536880-2','657054-000','700206725','760038240','760109462','760152587','760216762','760230938','760237050','760237876','760242369','760245401','760246283','760248521','760248527','760251048','790163-1','A14037-000','Consultancy Days','FBXLCUC11-MXF007','FFXLCLC42-MXF015','FGS-HMEC-A','FGS-HNTR-12MM','FGS-HNTR-16MM','FGS-MDSA-AB','FGS-MEXP-E-A/B/F','FGS-MFAW-A','FGS-MFAW-B','FGS-MHRT-A','FGS-MHRT-B','FGS-MSHS-A','Freight','ICX7150-24P-4X1G','KÖLCSDÍJ','LCSMDXKPT80M','ND3361.','NPC06UZDB-WT003M','NPC06UZDB-WT150C','NPC6ASZDB-GY050C','NPC6ASZDB-OR050C','NPC6ASZDB-WT010M','NPC6ASZDB-WT030M','NPC6ASZDB-WT050C','NPC6ASZDB-YL050C']
queries = ['6-641335-2','1-219106-5','NPC6ASZDB-WT005M','FFWLCLC42-JXF004','NCC44SZDB-08M015','NPC06UZDB-WT002M','1-1116412-3','2153449-2','2-599625-4','57535-2','NPC6ASZDB-WT003M','NPC6ASZDB-WT150C','1-6457567-6','1933286-4','760184820','NCC44SZDB-08M010','108232745','1-1933671-3','1375055-2','1-6536501-0','1671000-8','1671281-1','1671495-2','1671495-6','1673956-1.','1711797-1','1725150-3.','1725150-6.','2153437-1','2160046-5','2269081-4','2-336613-1','2843021-3','2-964830-1','2-966224-1','2-966740-1','5-336608-1','6-2843007-1','6536501-1','6536501-2','6536501-3','6536501-5','6536880-2','657054-000','700206725','760038240','760109462','760152587','760216762','760230938','760237050','760237876','760242369','760245401','760246283','760248521','760248527','760251048','790163-1','A14037-000','Consultancy Days','FBXLCUC11-MXF007','FFXLCLC42-MXF015','FGS-HMEC-A','FGS-HNTR-12MM','FGS-HNTR-16MM','FGS-MDSA-AB','FGS-MEXP-E-A/B/F','FGS-MFAW-A','FGS-MFAW-B','FGS-MHRT-A','FGS-MHRT-B','FGS-MSHS-A','Freight','ICX7150-24P-4X1G','KÖLCSDÍJ','LCSMDXKPT80M','ND3361.','NPC06UZDB-WT003M','NPC06UZDB-WT150C','NPC6ASZDB-GY050C','NPC6ASZDB-OR050C','NPC6ASZDB-WT010M','NPC6ASZDB-WT030M','NPC6ASZDB-WT050C','NPC6ASZDB-YL050C']
queries = ['599617-4','599619-4','599622-2','599622-4','599623-3','599624-4','599683-4','599690-2']

#Directory of downloaded specifications
specs_mappa = str(Path(__file__).parent.parent.absolute())+"\\specs\\"

#Downloading pdfs
for query in queries:

    if len(glob(f"{specs_mappa}{query.replace("/","-")}*.pdf")) > 0:
        continue
    try:
        #--Finding search bar--
        try:
            search_toggle = WebDriverWait(driver,1.5).until(EC.visibility_of_element_located((By.CLASS_NAME, "search-toggle")))
            search_toggle.click()
            waitabit()
            div = driver.find_element(By.CLASS_NAME, "mobile-search")
        except TimeoutException:
            div = driver.find_element(By.CLASS_NAME, "desktop-search")

        search_bar = div.find_element(By.CLASS_NAME, "search-bar")
        search_submit = div.find_element(By.CLASS_NAME, "search-submit-btn")

        #--Searching--
        search_bar.clear()
        search_bar.send_keys(query)
        waitabit()
        search_submit.click()

        wait_common.until(EC.text_to_be_present_in_element((By.CLASS_NAME, "search-hero-showing-results-text"), query)) #Waiting for results

        #--Downloading specification--

        try:
            card = wait_common.until(EC.visibility_of_element_located((By.XPATH, f"//*[contains(text(), '{query} Product specifications')]/../..")))
        except TimeoutException:
            print("\nProduct", query, "not found in time. Either the product doesn't have a specification available, or connection problems might have occurred.\n")
            continue

        # ha már létezik a fájl, akkor a régit töröljük
        files = glob(f"{specs_mappa}{query.replace("/","-")}*.pdf")
        if len(files) > 0: 
            for f in files:
                os.remove(f)

        card.find_element(By.CLASS_NAME, "download-btn").click()                                                #pressing download button
        waitabit()
        driver.switch_to.window(driver.window_handles[1])                                                       #changing tabs
        waitabit()
        hotkey('ctrl', 's')                                                                                     #saving pdf
        waitabit()
        hotkey('ctrl', 'c')                                                                                     #copying filename
        pyperclip.copy(specs_mappa+pyperclip.paste())    #putting path+filename on clipboard
        hotkey('ctrl', 'v')                                                                                     #pasting clipboard
        press('enter')                                                                                          #saving pdf
        sleep(2)
        press('esc')                                                                                            #closing download tab
        driver.close()                                                                                          #closing pdf tab
        driver.switch_to.window(driver.window_handles[0])                                                       #focusing on commscope site
    except Exception as e:
        print("\nHiba a",query,"specifikációjának letöltése közben:",e)
        continue

driver.quit()