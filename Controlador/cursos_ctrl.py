# controlador/cursos_ctrl.py
from typing import List, Optional
from modelo.entidades import Curso
from controlador.common import (
    CURSOS_FILE,
    MATRICULAS_FILE,
    cargar_datos_csv,
    guardar_datos_csv,
    cargar_datos_json
)


def obtener_cursos() -> List[Curso]:
    """Retorna la lista completa de cursos."""
    return cargar_datos_csv(CURSOS_FILE, Curso)


def obtener_curso_por_id(id_curso: str) -> Optional[Curso]:
    """Busca un curso por su ID."""
    for curso in obtener_cursos():
        if curso.id_curso == id_curso:
            return curso
    return None


def crear_curso(id_curso: str, nombre_curso: str, creditos: int) -> Curso:
    """Crea un nuevo curso y lo guarda."""
    if obtener_curso_por_id(id_curso):
        raise ValueError(f"El ID de curso '{id_curso}' ya existe.")

    nuevo = Curso(id_curso=id_curso, nombre_curso=nombre_curso, creditos=creditos)
    cursos = obtener_cursos()
    cursos.append(nuevo)
    guardar_datos_csv(CURSOS_FILE, cursos, ['id_curso', 'nombre_curso', 'creditos'])
    return nuevo


def actualizar_curso(id_original: str, nombre_curso: str, creditos: int) -> Optional[Curso]:
    """Actualiza los datos de un curso existente."""
    cursos = obtener_cursos()
    curso_encontrado = None
    for curso in cursos:
        if curso.id_curso == id_original:
            curso.nombre_curso = nombre_curso
            curso.creditos = creditos
            curso_encontrado = curso
            break

    if curso_encontrado:
        guardar_datos_csv(CURSOS_FILE, cursos, ['id_curso', 'nombre_curso', 'creditos'])
        return curso_encontrado
    else:
        raise ValueError(f"No se encontró un curso con ID '{id_original}'.")


def eliminar_curso(id_curso: str) -> bool:
    """Elimina un curso de la lista."""
    cursos = obtener_cursos()
    curso_a_eliminar = None
    for curso in cursos:
        if curso.id_curso == id_curso:
            curso_a_eliminar = curso
            break

    if curso_a_eliminar:
        # Validar que no esté en ninguna matrícula
        matriculas = cargar_datos_json(MATRICULAS_FILE)
        for m in matriculas:
            if id_curso in m.id_cursos:
                raise ValueError(f"No se puede eliminar. El curso está en la matrícula '{m.id_matricula}'.")

        cursos.remove(curso_a_eliminar)
        guardar_datos_csv(CURSOS_FILE, cursos, ['id_curso', 'nombre_curso', 'creditos'])
        return True
    else:
        raise ValueError(f"No se encontró un curso con ID '{id_curso}'.")