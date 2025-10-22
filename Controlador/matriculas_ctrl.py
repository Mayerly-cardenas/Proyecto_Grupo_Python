# controlador/matriculas_ctrl.py
from typing import List
from modelo.entidades import Estudiante, Matricula
from controlador.common import (
    MATRICULAS_FILE,
    cargar_datos_json,
    guardar_datos_json
)
from controlador import estudiantes_ctrl, cursos_ctrl


def matricular_estudiante(
        id_estudiante: str,
        id_cursos: List[str],
        periodo: str
) -> Matricula:
    """Crea una nueva matrícula para un estudiante."""
    # Validar que el estudiante exista
    if not estudiantes_ctrl.obtener_estudiante_por_id(id_estudiante):
        raise ValueError(f"El estudiante con ID '{id_estudiante}' no existe.")

    # Validar que todos los cursos existan
    cursos_validos = []
    for id_c in id_cursos:
        curso = cursos_ctrl.obtener_curso_por_id(id_c)
        if not curso:
            raise ValueError(f"El curso con ID '{id_c}' no existe.")
        cursos_validos.append(curso)

    matriculas = cargar_datos_json(MATRICULAS_FILE)

    # Generar un nuevo ID de matrícula
    nuevo_id = f"M{len(matriculas) + 1:03d}"

    nueva_matricula = Matricula(
        id_matricula=nuevo_id,
        id_estudiante=id_estudiante,
        periodo_academico=periodo,
        id_cursos=id_cursos
    )

    matriculas.append(nueva_matricula)
    guardar_datos_json(MATRICULAS_FILE, matriculas)
    return nueva_matricula


def obtener_matriculas_por_estudiante(id_estudiante: str) -> List[Matricula]:
    """Retorna todas las matrículas de un estudiante específico."""
    matriculas = cargar_datos_json(MATRICULAS_FILE)
    return [m for m in matriculas if m.id_estudiante == id_estudiante]


def obtener_estudiantes_por_curso(id_curso: str) -> List[Estudiante]:
    """Retorna todos los estudiantes matriculados en un curso específico."""
    matriculas = cargar_datos_json(MATRICULAS_FILE)
    estudiantes_en_curso = []
    id_estudiantes_en_curso = set()

    for m in matriculas:
        if id_curso in m.id_cursos:
            id_estudiantes_en_curso.add(m.id_estudiante)

    for id_est in id_estudiantes_en_curso:
        est = estudiantes_ctrl.obtener_estudiante_por_id(id_est)
        if est:
            estudiantes_en_curso.append(est)

    return estudiantes_en_curso


# --- Reto Final ---
def calcular_creditos_estudiante(id_estudiante: str, periodo: str) -> int:
    """Calcula el total de créditos matriculados por un estudiante en un período."""
    matriculas = obtener_matriculas_por_estudiante(id_estudiante)
    matricula_periodo = None
    for m in matriculas:
        if m.periodo_academico == periodo:
            matricula_periodo = m
            break

    if not matricula_periodo:
        return 0

    total_creditos = 0
    for id_c in matricula_periodo.id_cursos:
        curso = cursos_ctrl.obtener_curso_por_id(id_c)
        if curso:
            total_creditos += curso.creditos

    return total_creditos