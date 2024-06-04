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
7. Ejecuta Section 3.
8. Ejecutar la Section 4. Cambiar el nombre del archivo csv donde estan los ultimos datos old_df = pd.read_csv("data_15May_2024_all_stations.csv"). Y revisar que el nombre dir = "data_31May_2024_all_stations.csv" coincida con el del final_filename en donde se guardaron los nuevos datos.
9. Ejecutar la sección 9. Revisar los nombre de la carpeta de salida. Por default Los archivos finales se encontrarán en la carpeta "datos_por_estacion". Pero el csv de entrada de donde se toman los datos estará cambiando de nombre de acuerdo a la última actualizacion.

Segundo, hay que unirlos a los datos anteriores.

1. Actualizar el nombre de la carpeta con los nuevos datos más los anteriores de "datos_por_estacion" a "all_data_2005xstation_31_05_2024" (a la fecha correpsondiente)
2. En la celda 3 cambiar el nombre de la variable "dir_raw_data" con el nombre de la carpeta anterior (debe coincidir la fecha del último dato actualizado).
    Por ejemplo, el último dato anterior era del 15 de mayo por lo que la carpeta se llamaba "all_data_2005xstation_15_05_2024".
    Y esos datos se unirán con los nuevos, que son del 31 de mayo, por lo que la carpeta cambiará a:
    nuevo_nombre_carpeta = 'all_data_2005xstation_31_05_2024'  
2. Ejecutar el notebook completo  Actualizar_Datasets_(segmentar_en_train_test_validation).ipynb



## Para crear el archivo desde 0 con todos los datos

1. Descargar los datos de la página oficial
2. Abrir el archivo correccion_archivos_aireSalud.ipynb 
    2.1  Modificar SOLO en caso de ser necesario:
        El año, y el número de años a crear.
            Si por ejemplo se quieren crear carpetas desde el 2005 hasta el 2024, modificar year= 2005, y el for i in range(20)
3. Ejecutar todo hasta la Seccion 2 (correccion_archivos_aireSalud.ipynb )
4. Cambiar el nombre "final_filename" para guardar el archivo con los nuevos datos.
5. Ejecutar la sección 3.
5. SALTARSE LA 4 (ya que no hay datos previos). 
7. Ejecutar la sección 5. Los archivos finales se encontrarán en la carpeta "datos_por_estacion".

Segundo, hay que unirlos a los datos anteriores.

1. Mover a la carpeta el folder con los datos anteriores x estación "all_data_2005xstation_31_03_2024"
2. En la celda 2 cambiar el nombre de la variable "nuevo_nombre_carpeta" con la fecha del último dato actualizado.
    Por ejemplo, el último dato anterior era del 31 de marzo por lo que la carpeta se llamaba "all_data_2005xstation_31_03_2024".
    Y esos datos se unirán con los nuevos, que son del 15 de mayo, por lo que la carpeta cambiará a:
    nuevo_nombre_carpeta = 'all_data_2005xstation_15_05_2024'  
3. Ejecutar el notebook completo  Actualizar_Datasets_(segmentar_en_train_test_validation).ipynb
