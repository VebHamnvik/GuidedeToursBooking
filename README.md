# sent_g22

## Software Engineering & Testing 

### Gruppe 22 - Andrea, CT, Jørgen, Karoline & Vebjørn

#### Høgskolen i Østfold, høst 2023  


## Installering & kjøring av prototype
### 1. Last ned og pakk ut prosjektmappen.  
På Windows og Mac anbefaler vi å bruke 7zip https://7-zip.org/ for å pakke ut .zip mapper.
### 2. Last ned og installer python 3.10 og pip
#### Windows:   
Last ned python 3.10.11 installeren fra denne lenken: https://www.python.org/ftp/python/3.10.11/python-3.10.11-amd64.exe  
Kjør og trykk på “install now”. Dette installerer både python og pip.

#### Linux:
Dette er basert på at du bruker en debian-basert distribusjon. Stegene er antagligvis veldig like på andre distribusjoner.
Åpne en terminal og skriv følgende kommando:  
```bash
sudo apt install python3 python3-pip
```
#### MacOS:  
Lest ned python 3.10.11 installeren fra denne lenken:  
https://www.python.org/ftp/python/3.10.11/python-3.10.11-amd64.exe  
Kjør og installer.

### 3. Installer requirements:
Åpne prosjektmappen i terminal (mac & linux) eller powershell (windows).  
Kjør følgende kommando basert på operativsystem:  
#### Windows & Linux:
```bash
pip install -r requirements.txt
```
#### MacOS:
```bash
python3 -m pip install -r requirements.txt
```
### 4. Start prototypen
Åpne terminal (MacOS og Linux) eller powershell (Windows) i rotmappen til prosjektet.  
Kjør så følgende kommando:
#### Windows:
```bash
python main.py
```
#### Linux og MacOS:
```bash
python3 main.py
```
### 5. Åpne nettsiden i nettleseren din
Gå inn på lenken som blir skrevet ut i terminalen/powershell når programmet kjøres.  
Alternativt kan du trykke på denne lenken etter programmet er startet:  
http://localhost:5000/

Du har nå en kjørende versjon av prototypen i nettleseren din.


### 6. Innlogging
Dette er brukerinformasjon du kan bruke for å logge inn på ulike brukere.  
Denne informasjonen finner du også på login-siden vår.  
I vårt system har alle brukere tilgang til å lage annonser og booke turer.

**Både brukernavn og passord er alltid det samme  
(Eks. Brukernavn: *Guide1*, Passord: *Guide1*)**

### Her vil du se et eksempel på brukere som har laget annonser:  

| Brukernavn | Passord |
|------------|---------|
| Guide1     | Guide1  |
| Guide2     | Guide2  |
| Guide3     | Guide3  |


### Her vil du se et eksempel på en bruker som har booket noen turer

| Brukernavn | Passord |
|------------|---------|
| Bruker4     | Bruker4  |
| Bruker5     | Bruker5  |



## Kjøring av tester & coverage
### Coverage:
Åpne terminal eller powershell i rotmappen til prosjektet.  
Skriv følgende kommando for å kjøre tester med coverage:
```bash
coverage run -m pytest tests/
```
Kjør følgende kommando for å vise rapport for applikasjons-mappen.
```bash
coverage report -m --include='*/application/*'
```

### Pytest
Om du ønsker å kjøre pytest uten coverage kan du gjøre det også.
Da må du åpne terminal eller powershell i rotmappen til prosjektet.
Skriv så følgende kommando:
```bash
python3 -m pytest
```