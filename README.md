# PRA1 Web scraping
Aquest respositori conté el codi i les instruccions per a executar la PRA1 de l'assignatura Tipologia i cicle de vida de les dades a la Universitat Oberta de Catalunya (UOC).

Els integrants d'aquesta pràctica són:

* Ana Cortés Besolí
* Joan Oliva Costas

## Descripció General
L'aplicació és un web scraper que obté les dades de pel·lícules i crítiques d'[IMDB](https://www.imdb.com/). Per fer-ho, es cerquen les pàgines corresponents a les pel·lícules i les crítiques en funció dels paràmetres d'entrada. 

Amb l'ajuda de Selenium, es llegeix tota la informació de les pàgines i s'emmagatzema en el directori de sortida, que consisteix en un conjunt de fitxers .csv.

Per a executar el programa, si us plau feu-li una ullada al fitxer [Usage](usage.md) present en aquest mateix repositori de codi.

## Descripció dels fitxers
Els fitxers que composen el repositori són els següents:

* main.py: Punt d'entrada de l'aplicatiu. Llegeix els paràmetres d'entrada a partir de la configuració i invoca la lógica del scraper per tal d'escriure les dades en els fitxers de sortida.
* movies.py: Mòdul encarregat de cercar els identificadors de les pel·lícules a partir d'un títol i d'un any de llançament.
* movie.py: Mòdul encarregat de llegir les dades bàsiques de les pel·lícules.
* reviews.py: Mòdul encarregat d'obtenir la llista de crítiques de les pel·lícules.
* utils.py: Utilitats comuns de tots els móduls.
* copyConfig.py: Copia el fitxer config-sample.py cap al fitxer de producció config.py, que no és seguit pel repositori de codi.
* purgeOutput.py: Esborra els directoris de sortida de les execucions. 
* README.md: Aquest mateix fitxer de descripció.
* usage.md: Descripció dels requeriments i de com iniciar l'aplicació.

## Agraïments i llicència
Les dades que es pugin extreure amb l'ús de l'eina d'aquest repositori sols es poden utilitzar amb finalitats acadèmiques i sempre citant a IMBD com a autor original d'aquestes. No es permet cap ús comercial no autoritzat de les dades que es pugin extreure amb l'ús d'aquesta eina.

Així mateix, IMDB és l'autor original de les dades que es pugin extreure.

Agraïm a IMDB la seva cortesia per a la cesió de les dades, que sols disposen de finalitats acadèmiques.

Les dades que es puguin extreure amb aquest projecte es troben subjectes a la llicènia CC BY-NC-SA 4.0. 


## Data DOI
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.4155443.svg)](https://doi.org/10.5281/zenodo.4155443)



