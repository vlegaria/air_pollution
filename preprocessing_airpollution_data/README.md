# air_pollution
## Para agregar datos nuevos de las estaciones:

Primero hay que corregir el formato de los datos crudos (directamente descargados del Portal)

1. Descargar los datos de la página oficial
2. Abrir el archivo correccion_archivos_aireSalud.ipynb 
    2.1  Modificar SOLO en caso de ser necesario:
        El año, y el número de años a crear.
            Si solo se agregaran meses al 2024, dejar como está year = 2024 y el for i in range(1).
3. Cargar las librerías y ejecutar la Section1. Se crearán las carpetas en blanco correspondiente a cada contaminante.
4. Pegar en la carpeta "datos_Modificados" los archivos descargados en su año correspondiente y en su contaminante (el mes es indiferente, así como el nombre del archivo). 
5. Ejecutar la Seccion 2 (correccion_archivos_aireSalud.ipynb )
6. Cambiar el nombre "final_filename" para guardar el archivo con los nuevos datos.
7. Ejecuta Section 3 y Section 4. Los archivos finales se encontrarán en la carpeta "datos_por_estacion".

Segundo, hay que unirlos a los datos anteriores.

1. Mover a la carpeta el folder con los datos anteriores x estación "all_data_2005xstation_31_03_2024"
2. En la celda 2 cambiar el nombre de la variable "nuevo_nombre_carpeta" con la fecha del último dato actualizado.
    Por ejemplo, el último dato anterior era del 31 de marzo por lo que la carpeta se llamaba "all_data_2005xstation_31_03_2024".
    Y esos datos se unirán con los nuevos, que son del 15 de mayo, por lo que la carpeta cambiará a:
    nuevo_nombre_carpeta = 'all_data_2005xstation_15_05_2024'  
2. Ejecutar el notebook completo  Actualizar_Datasets_(segmentar_en_train_test_validation).ipynb



## Para crear el archivo desde 0 con todos los datos

1. Descargar los datos de la página oficial
2. Abrir el archivo correccion_archivos_aireSalud.ipynb 
    2.1  Modificar SOLO en caso de ser necesario:
        El año, y el número de años a crear.
            Si por ejemplo se quieren crear carpetas desde el 2005 hasta el 2024, modificar year= 2005, y el for i in range(20)
3. Ejecutar todo hasta la Seccion 2 (correccion_archivos_aireSalud.ipynb )
6. Cambiar el nombre "final_filename" para guardar el archivo con los nuevos datos.
7. Ejecuta Section 3 y Section 4. Los archivos finales se encontrarán en la carpeta "datos_por_estacion".

Segundo, hay que unirlos a los datos anteriores.

1. Mover a la carpeta el folder con los datos anteriores x estación "all_data_2005xstation_31_03_2024"
2. En la celda 2 cambiar el nombre de la variable "nuevo_nombre_carpeta" con la fecha del último dato actualizado.
    Por ejemplo, el último dato anterior era del 31 de marzo por lo que la carpeta se llamaba "all_data_2005xstation_31_03_2024".
    Y esos datos se unirán con los nuevos, que son del 15 de mayo, por lo que la carpeta cambiará a:
    nuevo_nombre_carpeta = 'all_data_2005xstation_15_05_2024'  
2. Ejecutar el notebook completo  Actualizar_Datasets_(segmentar_en_train_test_validation).ipynb
