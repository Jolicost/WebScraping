# Instal·lació i ús de l'aplicació
Per tal de poder llençar l'aplicació, es requereixen els següents components:

* Python > 3(es recomanda la versió 3.7)
* Pip (gestor de llibereríes). S'inclou dins de Python.
* Webdriver de Chrome/Firefox per a Selenium (explicat més endevant).
* Altres llibreríes (explicat més endevant).

## Instal·lació de llibreríes amb pip
Per a instal·lar les llibreríes necessaries per a executar els scripts, es pot optar per executar la comanda

pip install -r requierements.txt

## Webdriver de Selenium
El webdriver de Selenium permet que la liberería interaccioni amb el navegador. El reposiori suporta Chrome i Firefox, però requereix **disposar del driver (.exe) situat en la mateixa carpeta que la pràctica**.

Per a descarregar el driver adequat, es pot consultar el següent [enllaç](https://www.selenium.dev/downloads/#browsersExpand)

## Fitxer de configuració
El fitxer config-sample.yaml s'ha de renombrar cap a config.yaml (ignorat per git). Això es pot realitzar amb el fitxer de python inclós al repositori (copyConfig.py).

Un cop copiat, ja es pot executar el programa (main.py). Les claus de configuració s'expliquen a continuació:

* browser: navegador web utilitzat per selenium. Pot ser chrome/firefox.
* movies: Llistat de pel·lícules de les quals obtenir el dataset. Cada entrada consta de 2 atributs:
  * title: nom de la pel·lícula. Case insensitive. (obligatori)
  * year: any de la pel·lícula. Utilitzat per a filtrar pel·lícules amb el mateix títol però diferent any. (opcional)
* reviews: opcions d'extracció de les crítiques.
  * sort_by: patró per a obtenir les primeres crítiques. Pot prendre un dels següents valors:
    * helpfulness: puntuació de la crítica segons altres usuaris.
    * date: data de la crítica.
    * votes: vots totals de la crítica.
    * prolific: ordena les crítiques segons l'autor.
    * rating: puntuació de la pel·lícula segons la crítica.
  * sort_order: asc|desc segons com ordenar el criteri anterior.
  * max_reviews: nombre màxim de crítiques a obtenir d'una pel·lícula.
*debug: mode de depuració del programa. Evita realitzar tota l'execució si només es volen depurar algunes parts.
  * status: 1|0 segons si el mode de depuració és activat o no.
  * mode: mode de depuració seleccionat. Sols té sentit si la clau anterior és 1. Pot prendre els valors:
    * reviews: depuració de l'obtenció de les crítiques d'una pel·lícula.
	
## Natejar la sortida de dades
Cada vegada que es realitza una execució, es crea un directori a l'estil de dataset_timestamp" amb el resultat de l'execució.

Per a eliminar tots els directoris d'aquest tipus es pot executar el fitxer Python **purgeOutput.py**