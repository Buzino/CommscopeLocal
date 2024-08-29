CREATE DATABASE CommScopeLocal CHARACTER SET UTF8;

USE CommScopeLocal;

CREATE TABLE RAKTARAK (
    azon VARCHAR(8) PRIMARY KEY,
    varos VARCHAR(255),    
    orszag VARCHAR(255)
);

CREATE TABLE KESZLET (
    cikkszam VARCHAR(32),
    raktar VARCHAR(8),
    mennyiseg DECIMAL(15,5),
    mertekegyseg VARCHAR(16),
    lekerve DATE,
    PRIMARY KEY (cikkszam, raktar, lekerve),
    FOREIGN KEY (raktar) REFERENCES RAKTARAK(azon)
);

CREATE TABLE TULAJDONSAGOK (
    azon INT(10) PRIMARY KEY,
    megnevezes VARCHAR(255),
    mertekegyseg VARCHAR(16),
    kategoria VARCHAR(255)
);

CREATE TABLE SPECIFIKACIOK (
    cikkszam VARCHAR(32),
    tulajdonsag INT(10),
    ertek VARCHAR(512),
    ertek2 VARCHAR(16),
    PRIMARY KEY (cikkszam, tulajdonsag),
    FOREIGN KEY (tulajdonsag) REFERENCES TULAJDONSAGOK(azon)
);
