from glob import glob
import pymupdf, os
from pathlib import Path
import mysql.connector

def isFloat(str:str):
    try:
        float(str.replace(",",""))
        return True
    except ValueError:
        return False

def joinList(lista:list):
    joined = ""
    for x in lista:
        if type(x) in [list, set, tuple]:
            joined += " "+joinList(x)
        else:
            joined += " "+x
    return joined

def cleanUpList(lista:list):
    clean = []
    for x in lista:
        if type(x) in [list, set, tuple]:
            clean.append(cleanUpList(x))
        else:
            clean.append(x.strip().replace("\xa0","").replace("'","´").replace("\"","˝"))
    return clean

def uniqueList(lista:list):
    uniques = []
    for x in lista:
        if x not in uniques:
            uniques.append(x)
    return uniques

def cserel(uom:str):
    for x in cserelendo:
        uom = uom.replace(x[0], x[1])
    return uom

#keresendő cikkszámok
#matids = ['219413-2', '1375055-2', '1711163-1', '700214372', '760008888', '760237040', '884032314-10', '884061054-16', 'ck1828-001']
#matids = ['1375055-2']
#matids = ['CK1828-001','2111972-1','5-1375203-1','884061054/16','884032314/10','760239537','2111783-1','219413-2','1711327-1','EC6472-000','5-1912057-7','233131-1','1-2843020-1','737889-2','1375055-2','901-H550-US00','737890-1','1711053-1','760250556','2125101-1','760008888','760250560','700214372','810010020/DB','760250557','901-H550-US00']
#matids = ['9U1-R350-WW03','760246345','ICX7150-48PF-4RA','902-1170-AR00','60891121-06','NPC6ASZDB-YL001M','CV7092-000','1711732-3','E25G-SFP-TWX-P-51','760072959','740-64310-001','ICX7750-26Q','860644155','760246288','HST-B8HNA0150NN000','CPCSSZ2-06F025','740-64112-110','760245679','FGS-MH4E-H','ICX7000-C12-WMK','CA111K2-03F010','902-0173-AU00','760036293','ICX8200-48PF2-E2','ICX7150-C12P-2X10R','760230938','65772812-02','CC6325-000','BTM002-M14.0','760242750']

#letöltött specifikációk mappája
specs_mappa = str(Path(__file__).parent.parent.absolute())+"\\specs\\"

#cikkszámok kinyerése a specs mappából
matids = []

for x in glob(f'{specs_mappa}*.pdf'):
    y = x.removesuffix("-product-specifications.pdf").removesuffix("-product-specifications-comprehensive.pdf").removeprefix(specs_mappa)
    y = y.replace("-db","/DB").replace("-10","/10").replace("-16","/16").replace("-32","/32").replace("-00","/00")
    matids.append(y)

#változók
tulajdonsagok = []
specs = []

ertekek = []
tul = None
kateg = ""
me = ""
oldaltores = False
elozoek = None
vege = False
elozome = ""

cserelendo = [("in","mm"), ("lb","kg"), ("Vac","Vac/Vdc"), ("Vdc", "Vac/Vdc"), ("Vac/Vac","Vac"), ("Vdc/Vdc","Vdc")]

for matid in matids:

    vege = False
    megnevezes = []

    # legutoljára letöltött specifikáció megnyitása
    files = glob(f"{specs_mappa}{matid.replace("/","-")}*.pdf")
    if len(files) < 1:
        continue
    latest = max(files, key=os.path.getmtime)
    doc = pymupdf.open(latest)

    #végigciklizálunk az oldalakon, azok szövegblokkjain, sorain és szövegrészein
    #((nem tudom pontosan ez mi és miért, de reference-ből van, és működik))
    for page in doc:
        if vege: break
        blocks = page.get_text("dict", flags=11)["blocks"]
        for b in blocks:  # iterate through the text blocks
            if vege: break
            for l in b["lines"]:  # iterate through the text lines
                if vege: break
                for s in l["spans"]:  # iterate through the text spans

                    # a végén a certificate-eket egyelőre nem rakom bele
                    if s["text"] == "Agency":
                        vege = True
                        break

                    # Oldaltörésnél előfordul, hogy a következő tulajdonság értéke valamiért számunkra láthatatlanul szerepel
                    # az előző oldalon is, ezért az oldaltöréseket is követni kell, másképp problémás eredményt kapunk
                    if "Page" in s["text"] and "of" in s["text"]:
                        oldaltores = True

                    # a szövegek célját formázással különítem el
                    # a tulajdonságok 9-es betűméretűek
                    if s["size"] == 9:
                        # a tulajdonságok nevei vastagok (nem tudom, hogy működik a flags, de stackoverflow <3)
                        if s["flags"] & 2**4:

                            # ha van már tulajdonság"cím", akkor oldaltörésnél elmenti (ez az elején leírt probléma miatt kell)
                            # másképp pedig eltárolja a cikkszámhoz az adott tulajdonságot
                            if tul != None:
                                if oldaltores:
                                    elozoek = [matid, tul, ertekek, kateg, me, elozome]
                                else:
                                    tulajdonsagok.append((tul, kateg, cserel(me)))
                                    specs.append((matid, tul, ertekek))
                            
                            tul = s["text"]
                            ertekek = []
                            me = ""

                        # a tulajdonság értékei meg sima formázásúak
                        else:
                            # értékek feldolgozása
                            # itt néhány fontosabb sablon van külön feldolgozva
                            ertek = s["text"]
                            elozome = me

                            if s["text"].count("|") > 0:
                                metrikus = s["text"].split("|")[0].split(" ")
                                
                                if isFloat(metrikus[0]):
                                    ertek = metrikus[0]
                                    me = joinList(metrikus[1:])

                            elif s["text"].count("to") > 0 and s["text"].count("(") > 0:
                                felvagott = s["text"].split("(")[0].split("to")
                                if len(felvagott) >= 2:
                                    minimum = felvagott[0].strip().split(" ")
                                    maximum = felvagott[1].strip().split(" ")
                                    if len(minimum) >=2:
                                        me = minimum[1].strip()
                                    elif len(maximum) >= 2:
                                        me = maximum[1].strip()
                                    else:
                                        me = minimum[0]
                                    ertek = [minimum[0].strip(), maximum[0].strip()]

                            elif s["text"].count(" x ") > 0:
                                if s["text"].count("(") > 0:
                                    felvagott = s["text"].split("(")[0].split(" ")
                                else:
                                    felvagott = s["text"].split(" ")
                                
                                if isFloat(felvagott[0]) and isFloat(felvagott[2]):
                                    # [szam, x, szam, mm, ...]
                                    ertek1 = felvagott[0]
                                    ertek2 = felvagott[2]
                                    me = felvagott[3]
                                elif isFloat(felvagott[0]) and isFloat(felvagott[3]):
                                    # [szam, mm, x, szam, mm, ...]
                                    ertek1 = felvagott[0]
                                    ertek2 = felvagott[3]
                                    me = felvagott[1]
                                else:
                                    ertek1 = joinList(felvagott)
                                    ertek2 = ""
                                    me = ""
                                
                                ertek = [ertek1, ertek2]

                            else:
                                felvagott = s["text"].split(" ")

                                if len(felvagott) >= 2 and felvagott[0].count("–") == 1:
                                    me = felvagott[1]
                                    felvagott = felvagott[0].strip().split("–")
                                    if isFloat(felvagott[0]) and isFloat(felvagott[1]):
                                        ertek = [felvagott[0], felvagott[1]]
                                
                                elif len(felvagott) >= 4 and felvagott[1].count("–") > 0:
                                    me = felvagott[3]
                                    if isFloat(felvagott[0]) and isFloat(felvagott[2]):
                                        ertek = [felvagott[0], felvagott[2]]
                                
                                elif len(felvagott) > 1 and isFloat(felvagott[0]):
                                    ertek = felvagott[0]
                                    me = joinList(felvagott[1:])

                                else:
                                    ertek = joinList(felvagott)
                                    me = ""

                            ertekek.append(ertek)
                            
                            # oldaltörésnél ha az utolsó érték amit találtuk egyezik a mostanival,
                            # akkor az elejében leírt hibával találkozunk, erre megoldás ez a kód
                            if oldaltores and elozoek != None:
                                if len(elozoek[2]) > 0 and elozoek[2][-1] == ertek:
                                    elozoek[2].pop()  
                                specs.append((elozoek[0], elozoek[1], elozoek[2]))
                                tulajdonsagok.append((elozoek[1], elozoek[3], elozoek[5]))
                                oldaltores = False
                                elozoek = None

                    # ez a betűmérete a tulajdonságok kategóriáinak megnevezésének
                    elif s["size"] == 14.25:
                        kateg = s["text"]
                        if tul != None:
                            tulajdonsagok.append((tul, kateg, cserel(me)))
                            specs.append((matid, tul, ertekek))
                            tul = None
                            ertekek = []
                            me = ""
                            oldaltores = False
                            elozoek = None
                    
                    elif s["size"] == 12.75:
                        megnevezes.append(s["text"])

        specs.append((matid, "Product Name", megnevezes))
        tulajdonsagok.append(("Product Name", "", ""))

# Adatok feltöltése adatbázisba

tulajdonsagok = cleanUpList(tulajdonsagok)
specs = cleanUpList(specs)

try:

    db = mysql.connector.connect(
        host="localhost",
        username="root",
        password="",
        database="commscopelocal"
    )
    cursor = db.cursor(buffered=True)

    # baja van az sqlnek az idegen kulcsokkal, ez most nem érdekel minket <3
    cursor.execute("SET FOREIGN_KEY_CHECKS=0")
    db.commit()

    with open("baj.txt","w",encoding="utf-8") as f:
        for t in tulajdonsagok:
            f.write(str(t)+"\n")

    for t in uniqueList(tulajdonsagok):
        # ha már létezik a tulajdonság, akkor azt frissítjük
        cursor.execute(f"SELECT azon, mertekegyseg FROM tulajdonsagok WHERE megnevezes LIKE '{t[0]}'")
        sor = cursor.fetchone()
        
        if sor != None:
            azon = int(sor[0])
            me = sor[1]
        else:
            cursor.execute(f"SELECT MAX(azon) FROM tulajdonsagok")
            try:
                azon = int(cursor.fetchone()[0]) + 1
            except:
                azon = 1
            me = ""

        # ha eddig volt mértékegység és most ki akarná törölni a program, akkor megtartjuk a régit
        # ha van "új" m.e. (valszeg ugyanaz), akkor arra cseréljük
        if t[2] != "": me = t[2]
        
        cursor.execute(f"REPLACE INTO tulajdonsagok (azon, megnevezes, mertekegyseg, kategoria) VALUES ({azon},'{t[0]}','{me}','{t[1]}')")
        db.commit()

    cursor.execute("SET FOREIGN_KEY_CHECKS=1")
    db.commit()

    for s in specs:
        try:
            cikkszam = s[0]
            
            cursor.execute(f"SELECT azon FROM tulajdonsagok WHERE megnevezes LIKE '{s[1]}'")
            tulazon = cursor.fetchone()
            tulazon = tulazon[0]
            
            if len(s[2]) > 0 and type(s[2][0]) == list and len(s[2][0]) == 2  and isFloat(s[2][0][0]) and isFloat(s[2][0][1]):
                ertek1 = s[2][0][0]
                ertek2 = s[2][0][1]
            else:
                ertek1 = joinList(s[2])
                ertek2 = ""
            
            cursor.execute(f"REPLACE INTO specifikaciok (cikkszam, tulajdonsag, ertek, ertek2) VALUES ('{cikkszam}',{tulazon},'{ertek1.strip()}','{ertek2.strip()}')")
            db.commit()

        except Exception as e:
            print("Hiba SQL közben:",e,"\nsor:",s)
            continue

except Exception as e:
    print("\nHiba az adatbázisba feltöltés során:",e,"\n\n")

"""
SELECT cikkszam, megnevezes, ertek, ertek2, mertekegyseg
FROM specifikaciok INNER JOIN tulajdonsagok ON specifikaciok.tulajdonsag = tulajdonsagok.azon  
ORDER BY cikkszam, kategoria, megnevezes;

DELETE FROM specifikaciok;
DELETE FROM tulajdonsagok;
"""