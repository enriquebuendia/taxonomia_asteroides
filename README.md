# Clasificación taxonómica de asteroides
Repositorio para clasificar taxonómicamente asteroides con base a sus espectros de reflectancia en el rango de longitudes de onda de 4400-9200 Å, utilizando las taxonomías de Bus &amp; Binzel y Bus-DeMeo. 

Este script muestra las taxonomías correspondientes a las **10**, **30** y **50** menores _distancias espectrales_ calculadas al emparejar el espectro de interés y la base de datos SMASSII-E (para más información consulte el archivo pdf anexo), así también, con los espectros promedios de la clasificación Bus-DeMeo.    

### **Ejecución por Interfaz de Líneas de Comando (CLI)**

El script _main.py_ está diseñado para trabajar dentro de una terminal que se encuentre direccionada a la misma carpeta donde se descomprimio el script. Dentro de la carpeta de ejecución debe existir una subcarpeta con nombre: **_espectros_txt_**, donde se debe encontrar el archivo que contiene el espectro del asteroide de interés. 

La estructura del directorio debe verse similar a la siguiente forma:
```
taxonomia_asteroides-main
|   archivos.py
|   main.py
|   tools.py
|   README.md
|   requsitos.txt
|
|___/data
|       busdemeo-meanspectra.xlsx
|       tabla_smass.csv
|
|___/espectro_txt
|      a099942.hd078538_03_10.txt
|
|___/output
|      sumary_a099942.hd078538_03_10.txt
```

Para ejecutar el programa, una línea de comando típica puede verse así:

```python
python main.py nombre_archivo --smooth --nanometros
```

donde:
+ **nombre_archivo** Debe ser remplazado por el nombre del archivo que contiene al espectro de interés, el cual, debe de contener en su primera columna la longitud de onda, y en la segunda el flujo normalizado a 5500 Å. Son admitidos los formatos de archivo _.txt_ y _.csv_. Los delimitadores deben ser espacios en blanco. Los archivos no deben contener encabezados y los valores deben es tipo flotante (veasé [archivo de referencia](https://github.com/enriquebuendia/taxonomia_asteroides/blob/main/espectro_txt/a099942.hd078538_03_10.txt))  
+ **--smooth.** Bandera que debe ser activada si su espectro no ha sido suavizado previamente por un spline cúbico.
+ **--nanometros.** Por defecto, se espera que el archivo de entrada cuente con la longitud de onda medida en Angstroms, sin embargo, en caso de que el archivo se encuentre detallado en nanometros debe activarse esta bandera.

Otros parámetros pueden ser encontrados dentro de la ayuda proporcionada dentro del mismo script.

Se ha adjuntado un archivo con nombre: [a099942.hd078538_03_10.txt](https://github.com/enriquebuendia/taxonomia_asteroides/blob/main/espectro_txt/a099942.hd078538_03_10.txt), el cual es un ejemplo que contiene las características necesarias para que el programa sea ejecutado satisfactoriamente. Este espectro no ha sido suavizado y sus longitudes de onda se encuentran  en Angstroms.  

Este programa ha sido probado en los sistemas operativos Linux (_Ubuntu 20.04.2 LTS_) y MacOS () y bajo las librerias y versiones especificadas en el archivo [requisitos.txt](https://github.com/enriquebuendia/taxonomia_asteroides/blob/main/requisitos.txt).

#### **Archivos de salida**

Este programa puede proporcionar un archivo .txt con la información de las tres clasificaciones propuestas para las N menores _distancias espectrales_ ya mencionadas. Además, si lo desea, se pueden proporcionar las efemérides: _RA, DEC, delta_v, r, fase y V_. Nótese que de forma predeterminada estas efemerides son calculadas para el Observatorio Astrofísico Guillermo Haro (OAGH), por lo tanto, para especificar otra ubicación geográfica se debe modificar la matriz de localización del observador ubicada en la función _coordenadas2_ que se localiza dentro de [achivos.py](https://github.com/enriquebuendia/taxonomia_asteroides/blob/main/archivos.py) (Para mayor información  consulte la documentación de [astroquery](https://astroquery.readthedocs.io/en/latest/mpc/mpc.html)). Todos los archivos de resumen se podrán encontra dentro de la carpeta [output](https://github.com/enriquebuendia/taxonomia_asteroides/tree/main/output)
      

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
