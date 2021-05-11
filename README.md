# Clasificación taxonomica de asteroides
Repositorio para clasificar taxonomicamente asteroides con base a su espectros de reflectancia en el rango de longitudes de onda de 4400 - 9200 Å, utilizando las taxonomías de Bus &amp; Binzel (2002a, 2002b) y Bus-DeMeo (2009). Este script sólo muestra las taxonomías correspondientes a las 10 menores distancias espectrales calculadas al emparejar el espectro de interés y la base de datos SMASSII-E (para mas información consulte el archivo pdf anexo).    

### **Ejecución por Interfaz de Líneas de Comando (CLI)**

El script _main.py_ está diseñado para clasificar el espectro de un asteroide mediante las dos taxonomías mencionadas.

Para ejecutar el programa, una línea de comando típica puede verse así:

```python
python main.py archivo.txt --smooth --nanometros
```

donde:
+ **archivo.txt.** Debe ser remplazado por el nombre del archivo que contiene el espectro a analizar, el cual debe de contener en su primera columna la longitud de onda y en la segunda el flujo normalizado a 5500 Å.
+ **--smooth.** Bandera que debe ser activada si su espectro no ha sido suavizado, previamente, por un spline cúbico.
+ **--nanometros.** Por defecto, se espera que el archivo de entrada cuente con la longitud de onda medida en Angstroms, sin embargo, en caso de que el archivo se encuentre calibrado en nanometros debe activarse esta bandera.

Otros parámetros puede ser encontrados dentro de la ayuda proporcionada dentro del mismo script.

### **Cita**

Si usted cuenta útil este trabajo para su investigación, puede citarse como:
```
@mastersthesis{buendia2021taxo,
  title={Clasificación taxonómica de asteroides de la familia Flora},
  author={Buendia-Verdiguel, Enrique},
  school={Instituto Nacional de Astrofísica, Óptica y Electrónica},
  year={2021}
}
```
### Preguntas o comentarios ###

Siéntase libre de realizar cualquier comentario o pregunta a través de este repositorio o por medio del correo electrónico: _enriquebuendiav@gmail.com_  
