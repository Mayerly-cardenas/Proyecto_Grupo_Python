# tests/test_estudiantes.py
import pytest
import os
import csv
import json
# Importa todos los controladores que interactuarán
from controlador import estudiantes_ctrl, cursos_ctrl, matriculas_ctrl, common
from modelo.entidades import Estudiante, Curso, Matricula


# --- Fixture de configuración ---

@pytest.fixture
def setup_test_data(tmp_path):
    """
    Crea archivos temporales para las pruebas y "parchea" (modifica) las rutas
    que usa el controlador para que apunten a estos archivos de prueba.
    """
    # Guardamos las rutas originales para restaurarlas después
    original_est_file = common.ESTUDIANTES_FILE
    original_cur_file = common.CURSOS_FILE
    original_mat_file = common.MATRICULAS_FILE

    # Creamos un directorio 'data' temporal
    temp_data_dir = tmp_path / "data"
    temp_data_dir.mkdir()

    # Creamos las rutas a los archivos temporales
    temp_est_file = temp_data_dir / "estudiantes.csv"
    temp_cur_file = temp_data_dir / "cursos.csv"
    temp_mat_file = temp_data_dir / "matriculas.json"

    # Escribimos datos de prueba en los archivos temporales
    with open(temp_est_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['id_estudiante', 'nombre', 'carrera'])
        writer.writerow(['E100', 'Estudiante Prueba', 'Carrera Prueba'])

    with open(temp_cur_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['id_curso', 'nombre_curso', 'creditos'])
        writer.writerow(['C100', 'Curso Prueba', '3'])

    with open(temp_mat_file, 'w') as f:
        json.dump([], f)  # Empezamos sin matrículas

    # Sobrescribimos las constantes en el módulo 'common'
    common.ESTUDIANTES_FILE = str(temp_est_file)
    common.CURSOS_FILE = str(temp_cur_file)
    common.MATRICULAS_FILE = str(temp_mat_file)

    # 'yield' entrega el control a la función de prueba
    yield

    # --- Limpieza ---
    # Esto se ejecuta DESPUÉS de cada prueba
    # Restauramos las rutas originales para no afectar otras pruebas
    common.ESTUDIANTES_FILE = original_est_file
    common.CURSOS_FILE = original_cur_file
    common.MATRICULAS_FILE = original_mat_file


# --- Pruebas de Estudiantes ---

def test_cargar_estudiantes(setup_test_data):
    """Prueba que los estudiantes se carguen correctamente."""
    estudiantes = estudiantes_ctrl.obtener_estudiantes()
    assert len(estudiantes) == 1
    assert estudiantes[0].id_estudiante == "E100"
    assert estudiantes[0].nombre == "Estudiante Prueba"


def test_crear_estudiante(setup_test_data):
    """Prueba la creación de un nuevo estudiante."""
    estudiantes_ctrl.crear_estudiante("E101", "Nuevo Estudiante", "Nueva Carrera")
    estudiantes = estudiantes_ctrl.obtener_estudiantes()
    assert len(estudiantes) == 2
    assert estudiantes[1].id_estudiante == "E101"


def test_crear_estudiante_duplicado_falla(setup_test_data):
    """Prueba que no se pueda crear un estudiante con ID duplicado."""
    # Esperamos que esta acción lance un 'ValueError'
    with pytest.raises(ValueError, match="ya existe"):
        estudiantes_ctrl.crear_estudiante("E100", "Otro Nombre", "Otra Carrera")


def test_obtener_estudiante_no_existente(setup_test_data):
    """Prueba que buscar un ID inexistente retorne None."""
    est = estudiantes_ctrl.obtener_estudiante_por_id("E999")
    assert est is None


def test_actualizar_estudiante(setup_test_data):
    """Prueba la actualización de un estudiante."""
    estudiantes_ctrl.actualizar_estudiante("E100", "Nombre Actualizado", "Carrera Actualizada")
    est = estudiantes_ctrl.obtener_estudiante_por_id("E100")
    assert est is not None
    assert est.nombre == "Nombre Actualizado"
    assert est.carrera == "Carrera Actualizada"


def test_eliminar_estudiante_sin_matricula(setup_test_data):
    """Prueba la eliminación de un estudiante que no tiene matrículas."""
    estudiantes_ctrl.eliminar_estudiante("E100")
    estudiantes = estudiantes_ctrl.obtener_estudiantes()
    assert len(estudiantes) == 0


def test_eliminar_estudiante_con_matricula_falla(setup_test_data):
    """
    Prueba que no se pueda eliminar un estudiante si tiene una matrícula activa.
    Esta es una prueba de "integridad de datos".
    """
    # Se necesita crear una matrícula para el estudiante E100
    matriculas_ctrl.matricular_estudiante("E100", ["C100"], "2025-T1")

    # Ahora intentamos borrar el estudiante
    with pytest.raises(ValueError, match="tiene 1 matrícula"):
        estudiantes_ctrl.eliminar_estudiante("E100")