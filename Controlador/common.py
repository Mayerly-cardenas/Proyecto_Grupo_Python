# controlador/common.py
import csv
import json
import os
from typing import List, Any
from modelo.entidades import Curso, Matricula

# --- Constantes de Archivos ---
# Esto encuentra la raíz del proyecto (un nivel arriba de 'controlador')
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
ESTUDIANTES_FILE = os.path.join(DATA_DIR, "estudiantes.csv")
CURSOS_FILE = os.path.join(DATA_DIR, "cursos.csv")
MATRICULAS_FILE = os.path.join(DATA_DIR, "matriculas.json")


# --- Funciones de Carga y Guardado ---

def cargar_datos_csv(archivo: str, modelo: type) -> List[Any]:
    """Carga datos desde un archivo CSV y los convierte a una lista de modelos."""
    datos = []
    try:
        with open(archivo, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for fila in reader:
                # Convertir créditos a int si el modelo es Curso
                if modelo == Curso and 'creditos' in fila:
                    try:
                        fila['creditos'] = int(fila['creditos'])
                    except ValueError:
                        print(f"Advertencia: Crédito no válido para {fila.get('nombre_curso')}")
                        continue
                datos.append(modelo(**fila))
    except FileNotFoundError:
        print(f"Advertencia: Archivo no encontrado {archivo}. Se creará uno nuevo al guardar.")
    except Exception as e:
        print(f"Error inesperado al cargar {archivo}: {e}")
    return datos

def guardar_datos_csv(archivo: str, datos: List[Any], encabezados: List[str]):
    """Guarda una lista de modelos en un archivo CSV."""
    try:
        with open(archivo, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=encabezados)
            writer.writeheader()
            for item in datos:
                writer.writerow(item.__dict__)
    except IOError as e:
        print(f"Error al escribir en {archivo}: {e}")

def cargar_datos_json(archivo: str) -> List[Matricula]:
    """Carga datos desde un archivo JSON y los convierte a una lista de Matricula."""
    datos = []
    try:
        with open(archivo, mode='r', encoding='utf-8') as f:
            lista_json = json.load(f)
            for item in lista_json:
                datos.append(Matricula(**item))
    except FileNotFoundError:
        print(f"Advertencia: Archivo no encontrado {archivo}. Se creará uno nuevo al guardar.")
    except json.JSONDecodeError:
        print(f"Advertencia: Archivo JSON {archivo} está vacío o corrupto.")
    except Exception as e:
        print(f"Error inesperado al cargar {archivo}: {e}")
    return datos

def guardar_datos_json(archivo: str, datos: List[Matricula]):
    """Guarda una lista de modelos Matricula en un archivo JSON."""
    try:
        with open(archivo, mode='w', encoding='utf-8') as f:
            lista_dict = [item.__dict__ for item in datos]
            json.dump(lista_dict, f, indent=2)
    except IOError as e:
        print(f"Error al escribir en {archivo}: {e}")