# modelo/entidades.py
from dataclasses import dataclass, field
from typing import List

@dataclass
class Estudiante:
    id_estudiante: str
    nombre: str
    carrera: str

@dataclass
class Curso:
    id_curso: str
    nombre_curso: str
    creditos: int  # Los créditos son numéricos

@dataclass
class Matricula:
    id_matricula: str
    id_estudiante: str
    periodo_academico: str
    # Usamos field para inicializar la lista vacía si no se provee
    id_cursos: List[str] = field(default_factory=list)