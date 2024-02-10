# crawler v1.0
# Autor: Andrés González Méndez
# Fecha: 12/02/2024

import argparse
import csv
import itertools
import requests
from bs4 import BeautifulSoup
from io import TextIOWrapper

def main():
    """Script principal"""
    # Obtener valores de los parámetros
    parameters = get_parameters()

    file_name = parameters["file_name"]
    start = parameters["start"]
    count = parameters["count"]

    # Abrir archivo csv
    with open(file_name, 'r', encoding="utf8") as csvfile:
        # Extraer subconjunto de líneas del archivo csv
        reader = get_subset_from_csv(csvfile, start, count)

        # Obtener lista con los dominios
        domain_list = get_list_of_domains(reader)

    # Añadir esquema "https" a las urls
    url_list = add_scheme_to_url(domain_list)

    # Realizar llamada a las urls para obtener títulos html
    title_list = get_web_title(url_list)

    # Contar número de letras 'c' en cada título
    c_count = count_characters_in_string(title_list, 'c')
    
    # Mostrar resultados por pantalla
    print_out_results(domain_list, c_count)

def get_parameters() -> dict:
    """Lee los parámetros introducidos por el usuario y devuelve un diccionario con sus valores.
    Raises:
        ValueError: Si algún parámetro es incorrecto.
    Returns:
        dict: Diccionario con todos los parámetros y sus valores.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", required=True, help="Ruta del fichero")
    parser.add_argument("-c", "--count", help="Número de webs (opcional)")
    parser.add_argument("-s", "--start", help="Ranking inicial (opcional)")

    arguments = vars(parser.parse_args())

    file_name = arguments["file"]

    if not arguments["start"]:
        start = None
    elif not arguments["start"].isdigit():
        raise ValueError("El parámetro -s debe ser un entero mayor o igual que 1")
    else:
        start = int(arguments["start"])

    if not arguments["count"]:
        count = None
    elif not arguments["count"].isdigit():
        raise ValueError("El parámetro -c debe ser un entero mayor o igual que 1")
    else:
        count = int(arguments["count"])

    return {"file_name": file_name, "start": start, "count": count}
                
def get_subset_from_csv(csvfile: TextIOWrapper, start: int = None, count: int = None):
    """Extrae un subconjunto de líneas de un fichero csv.
    Args:
        csvfile (TextIOWrapper): Archivo csv.
        start (int, optional): Número de línea a partir de la cual se extraen los datos.
            Si es None, se extrae desde la primera línea.
        count (int, optional): Número de líneas que se extraen. Defaults to None.
            Si es None, se extrae hasta el final del archivo.
    Returns:
        Objeto iterable formado por el conjunto de líneas extraídas del archivo csv.
    """
    reader = csv.reader(csvfile)
    next(reader)

    if count and start:
        return itertools.islice(reader, start-1, start+count-1)
    elif count and not start:
        return itertools.islice(reader, 0, count)
    elif not count and start:
        return itertools.islice(reader, start-1, None)
    else:
        return reader

def get_list_of_domains(reader) -> list:
    """Recibe un objeto iterable formado por líneas extraídas de un archivo csv y devuelve una lista con los dominios de cada línea.
    Args:
        reader: Objeto iterable formado por líneas extraídas de un archivo csv.
    Returns:
        list: Lista formada por los dominios extraídos de cada una de las líneas del objeto de entrada.
    """
    domains = []

    for row in reader:
        domains.append(row[2])

    return domains

def add_scheme_to_url(domain_list: list, scheme: str = "https") -> list:
    """Añade el esquema deseado a todos los dominios incluidos en una lista.
    Args:
        domain_list (list): Lista formada por dominios.
        scheme (str, optional): Esquema a añadir a los dominios. Por defecto "https".
    Returns:
        list: Lista formada por urls generadas a partir del esquema y los dominios.
    """
    urls_with_scheme = []

    for url in domain_list:
        url_with_scheme = f"{scheme}://{url}"
        urls_with_scheme.append(url_with_scheme)

    return urls_with_scheme

def get_web_title(url_list: list) -> list:
    """Hace una petición a cada url y devuelve una lista con los títulos html recibidos
    Args:
        url_list (list): Lista con todas las urls a las que realizar la petición.
    Returns:
        list: Lista con los títulos html recibidos
    """
    titles = []

    for url in url_list:
        try:
            response = requests.get(url)
        except:
            titles.append(None)
        else:
            soup = BeautifulSoup(response.text, 'html.parser')
            title = soup.find('title')
            titles.append(title.get_text()) if title else titles.append(None)
        
    return titles

def count_characters_in_string(data: list, char: str) -> list:
    """Cuenta el número de apariciones de un caracter en cada elemento de una lista
    Args:
        data (list): Lista sobre la que se realiza la cuenta.
        char (str): Caracter que se contabiliza en la lista.
    Returns:
        list: Lista formada por el número de apariciones del caracter en cada elemento.
    """
    count = []

    for element in data:
        count.append(element.upper().count(char.upper())) if element else count.append(None)

    return count

def print_out_results(domain_list: list, count_list: list):
    """Imprime en pantalla el resultado final. 
    Args:
        domain_list (list): Lista formada por dominios.
        count_list (list): Lista formada por el número de apariciones del caracter en cada elemento.
    """
    for i, domain in enumerate(domain_list):
        count = count_list[i]

        if count is not None:
            output = f"{domain} tiene {count} letras c en su título"
        else:
            output = f"{domain} no se pudo obtener título html"

        print(output)

if __name__ == "__main__":
    main()
