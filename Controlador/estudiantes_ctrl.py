# controlador/estudiantes_ctrl.py
from typing import List, Optional
from modelo.entidades import Estudiante
from controlador.common import (
    ESTUDIANTES_FILE,
    cargar_datos_csv,
    guardar_datos_csv,
)
# Necesitaremos esto para la validación de borrado
from controlador import matriculas_ctrl


def obtener_estudiantes() -> List[Estudiante]:
    """Retorna la lista completa de estudiantes."""
    return cargar_datos_csv(ESTUDIANTES_FILE, Estudiante)


def obtener_estudiante_por_id(id_estudiante: str) -> Optional[Estudiante]:
    """Busca un estudiante por su ID."""
    for est in obtener_estudiantes():
        if est.id_estudiante == id_estudiante:
            return est
    return None


def crear_estudiante(id_estudiante: str, nombre: str, carrera: str) -> Estudiante:
    """Crea un nuevo estudiante y lo guarda."""
    if obtener_estudiante_por_id(id_estudiante):
        raise ValueError(f"El ID de estudiante '{id_estudiante}' ya existe.")

    nuevo = Estudiante(id_estudiante=id_estudiante, nombre=nombre, carrera=carrera)
    estudiantes = obtener_estudiantes()
    estudiantes.append(nuevo)
    guardar_datos_csv(ESTUDIANTES_FILE, estudiantes, ['id_estudiante', 'nombre', 'carrera'])
    return nuevo


def actualizar_estudiante(id_original: str, nombre: str, carrera: str) -> Optional[Estudiante]:
    """Actualiza los datos de un estudiante existente."""
    estudiantes = obtener_estudiantes()
    estudiante_encontrado = None
    for est in estudiantes:
        if est.id_estudiante == id_original:
            est.nombre = nombre
            est.carrera = carrera
            estudiante_encontrado = est
            break

    if estudiante_encontrado:
        guardar_datos_csv(ESTUDIANTES_FILE, estudiantes, ['id_estudiante', 'nombre', 'carrera'])
        return estudiante_encontrado
    else:
        raise ValueError(f"No se encontró un estudiante con ID '{id_original}'.")


def eliminar_estudiante(id_estudiante: str) -> bool:
    """Elimina un estudiante de la lista."""
    estudiantes = obtener_estudiantes()
    estudiante_a_eliminar = None
    for est in estudiantes:
        if est.id_estudiante == id_estudiante:
            estudiante_a_eliminar = est
            break

    if estudiante_a_eliminar:
        # Validar que no tenga matrículas activas
        matriculas = matriculas_ctrl.obtener_matriculas_por_estudiante(id_estudiante)
        if matriculas:
            raise ValueError(f"No se puede eliminar. El estudiante tiene {len(matriculas)} matrícula(s) asociada(s).")

        estudiantes.remove(estudiante_a_eliminar)
        guardar_datos_csv(ESTUDIANTES_FILE, estudiantes, ['id_estudiante', 'nombre', 'carrera'])
        return True
    else:
        raise ValueError(f"No se encontró un estudiante con ID '{id_estudiante}'.")