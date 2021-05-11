# Clasificación taxonómica de asteroides
Repositorio para clasificar taxonómicamente asteroides con base a sus espectros de reflectancia en el rango de longitudes de onda de 4400-9200 Å, utilizando las taxonomías de Bus &amp; Binzel y Bus-DeMeo. 

Este script sólo muestra las taxonomías correspondientes a las 10 menores distancias espectrales calculadas al emparejar el espectro de interés y la base de datos SMASSII-E (para mas información consulte el archivo pdf anexo), asi como también con los espectros promedios de la clasificación Bus-DeMeo.    

### **Ejecución por Interfaz de Líneas de Comando (CLI)**

El script _main.py_ está diseñado para trabajar dentro de una terminal que se encuentre direccionado a la misma carpeta donde se descomprimio el script. Dentro de la carpeta de ejecución debe existir una subcarpeta con nombre **_espectros_txt_** donde se debe encontrar el archivo que contiene el espectro del asteroide de interés. 

La estructura de los directorios debe verse de la siguiente forma:
```
taxonomia_asteroides-main
|   busdemeo-meanspectra.xlsx
|   main.py
|   tabla_smass.csv
|   tools.py
|   README.md
|   requsitos.txt
|
|___espectro_txt
    |   espectro_1.txt
    |   espectro_2.txt
    |   
    .
    .
    .
    |   espectro_n.txt
```

Para ejecutar el programa, una línea de comando típica puede verse así:

```python
python main.py espectro_1.txt --smooth --nanometros
```

donde:
+ **espectro_1.txt.** Debe ser remplazado por el nombre del archivo que contiene el espectro a analizar, el cual debe de contener en su primera columna la longitud de onda y en la segunda el flujo normalizado a 5500 Å.
+ **--smooth.** Bandera que debe ser activada si su espectro no ha sido suavizado previamente por un spline cúbico.
+ **--nanometros.** Por defecto, se espera que el archivo de entrada cuente con la longitud de onda medida en Angstroms, sin embargo, en caso de que el archivo se encuentre detallado en nanometros debe activarse esta bandera.

Otros parámetros pueden ser encontrados dentro de la ayuda proporcionada dentro del mismo script.

Este programa ha sido probado en los sistemas operativos Linux (_Ubuntu 20.04.2 LTS_) y MacOS () y bajo las librerias y versiones especificadas en el archivo [requisitos.txt](https://github.com/enriquebuendia/taxonomia_asteroides/blob/main/requisitos.txt). 

### **Cita**

Si usted encuentra útil este trabajo para su investigación, puede citarse como:
```
@mastersthesis{buendia2021,
  title={Clasificación taxonómica de asteroides de la familia Flora},
  author={Buendia, Enrique},
  school={Instituto Nacional de Astrofísica, Óptica y Electrónica},
  year={2021}
}
```
### Preguntas o comentarios ###

Siéntase libre de realizar cualquier comentario o pregunta a través de este repositorio o por medio del correo electrónico: _enriquebuendiav@gmail.com_  
