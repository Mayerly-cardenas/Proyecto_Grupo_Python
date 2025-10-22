# tests/test_cursos.py
import pytest
import csv
import json
from controlador import estudiantes_ctrl, cursos_ctrl, matriculas_ctrl, common


# --- Fixture ---
# Este fixture se puede copiar en cada archivo de prueba
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


# --- Pruebas de Cursos ---

def test_cargar_cursos(setup_test_data):
    """Prueba que los cursos se carguen y los créditos se conviertan a int."""
    cursos = cursos_ctrl.obtener_cursos()
    assert len(cursos) == 1
    assert cursos[0].id_curso == "C100"
    assert cursos[0].creditos == 3  # Verificar conversión a int


def test_crear_curso(setup_test_data):
    """Prueba la creación de un nuevo curso."""
    cursos_ctrl.crear_curso("C101", "Curso Nuevo", 4)
    cursos = cursos_ctrl.obtener_cursos()
    assert len(cursos) == 2
    assert cursos[1].id_curso == "C101"
    assert cursos[1].creditos == 4


def test_eliminar_curso_con_matricula_falla(setup_test_data):
    """Prueba que no se pueda eliminar un curso si está en una matrícula."""
    # Primero matriculamos un estudiante en el curso
    matriculas_ctrl.matricular_estudiante("E100", ["C100"], "2025-T1")

    # Ahora intentamos borrar el curso
    with pytest.raises(ValueError, match="El curso está en la matrícula 'M001'"):
        cursos_ctrl.eliminar_curso("C100")