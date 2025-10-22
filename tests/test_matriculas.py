# tests/test_matriculas.py
import pytest
import csv
import json
from controlador import estudiantes_ctrl, cursos_ctrl, matriculas_ctrl, common


# --- Fixture ---
@pytest.fixture
def setup_test_data(tmp_path):
    original_est_file = common.ESTUDIANTES_FILE
    original_cur_file = common.CURSOS_FILE
    original_mat_file = common.MATRICULAS_FILE
    temp_data_dir = tmp_path / "data"
    temp_data_dir.mkdir()
    temp_est_file = temp_data_dir / "estudiantes.csv"
    temp_cur_file = temp_data_dir / "cursos.csv"
    temp_mat_file = temp_data_dir / "matriculas.json"
    with open(temp_est_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['id_estudiante', 'nombre', 'carrera'])
        writer.writerow(['E100', 'Estudiante Prueba', 'Carrera Prueba'])
    with open(temp_cur_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['id_curso', 'nombre_curso', 'creditos'])
        writer.writerow(['C100', 'Curso Prueba', '3'])
    with open(temp_mat_file, 'w') as f:
        json.dump([], f)
    common.ESTUDIANTES_FILE = str(temp_est_file)
    common.CURSOS_FILE = str(temp_cur_file)
    common.MATRICULAS_FILE = str(temp_mat_file)
    yield
    common.ESTUDIANTES_FILE = original_est_file
    common.CURSOS_FILE = original_cur_file
    common.MATRICULAS_FILE = original_mat_file


# --- Pruebas de Matrículas y Reportes ---

def test_matricular_estudiante(setup_test_data):
    """Prueba la lógica de matriculación."""
    matriculas_ctrl.matricular_estudiante("E100", ["C100"], "2025-T1")
    # Leemos directamente del archivo JSON de prueba
    matriculas = common.cargar_datos_json(common.MATRICULAS_FILE)

    assert len(matriculas) == 1
    assert matriculas[0].id_matricula == "M001"
    assert matriculas[0].id_estudiante == "E100"
    assert matriculas[0].id_cursos == ["C100"]


def test_matricular_estudiante_curso_no_existe_falla(setup_test_data):
    """Prueba que la matrícula falle si un curso no existe."""
    with pytest.raises(ValueError, match="curso con ID 'C999' no existe"):
        matriculas_ctrl.matricular_estudiante("E100", ["C100", "C999"], "2025-T1")


def test_calcular_creditos_estudiante_reto_final(setup_test_data):
    """Prueba el reto final de calcular créditos."""
    # Matriculamos en período 1
    matriculas_ctrl.matricular_estudiante("E100", ["C100"], "2025-T1")

    # Creamos otro curso y matriculamos en período 2
    cursos_ctrl.crear_curso("C101", "Curso Avanzado", 5)
    matriculas_ctrl.matricular_estudiante("E100", ["C101"], "2025-T2")

    # Probar créditos del período 1 (Debe dar 3)
    creditos_t1 = matriculas_ctrl.calcular_creditos_estudiante("E100", "2025-T1")
    assert creditos_t1 == 3

    # Probar créditos del período 2 (Debe dar 5)
    creditos_t2 = matriculas_ctrl.calcular_creditos_estudiante("E100", "2025-T2")
    assert creditos_t2 == 5


def test_obtener_estudiantes_por_curso(setup_test_data):
    """Prueba el reporte de estudiantes por curso."""
    matriculas_ctrl.matricular_estudiante("E100", ["C100"], "2025-T1")

    estudiantes = matriculas_ctrl.obtener_estudiantes_por_curso("C100")
    assert len(estudiantes) == 1
    assert estudiantes[0].id_estudiante == "E100"

    # Probar un curso sin estudiantes
    estudiantes_vacios = matriculas_ctrl.obtener_estudiantes_por_curso("C999")
    assert len(estudiantes_vacios) == 0