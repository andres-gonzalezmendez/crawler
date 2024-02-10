# Ejercicio "crawler"

Autor: Andrés González Méndez

Fecha: 12/02/2024

## Antes de ejecutar el script

- Descarga e instala Python: https://www.python.org/downloads/
- Descarga el repositorio a una carpeta de tu ordenador.
- Abre el terminal en esa carpeta.
- Crea un entorno virtual:
  ```
  python -m venv venv
  ```
- Activa el entorno virtual:

  En Windows, ejecuta:
  ```
  venv\Scripts\activate
  ```
  En Unix o MacOS, ejecuta:
  ```
  venv/bin/activate
  ```
- Instala los paquetes necesarios para el correcto funcionamiento del script:
  ```
  pip install -r requirements.txt
  ```

## Cómo ejecutar el script

- Ejecuta el script con el siguiente comando:
  ```
  python crawler.py -f <ruta_fichero_csv> -s <s> -c <c>
  ```
  Donde:
  + `s`: Número de ranking de la web a partir de la cual se inicia la consulta.
  + `c`: Número de webs que se incluirán en la consulta.
 
## Obtener ayuda

- Ejecuta el script con el siguiente argumento:
  ```
  python crawler.py -h
  ```