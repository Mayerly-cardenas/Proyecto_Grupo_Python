from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt, IntPrompt
from typing import List, Optional
# Importa las clases de tu archivo de modelos
from modelo.entidades import Estudiante, Curso, Matricula

# Inicializar la consola de rich
consola = Console()


def mostrar_error(mensaje: str):
    """Muestra un mensaje de error formateado."""
    consola.print(Panel(f"❌ {mensaje}", title="[bold red]Error[/bold red]", border_style="red"))


def mostrar_exito(mensaje: str):
    """Muestra un mensaje de éxito formateado."""
    consola.print(Panel(f"✅ {mensaje}", title="[bold green]Éxito[/bold green]", border_style="green"))


def mostrar_menu_principal() -> str:
    """Muestra el menú principal y solicita una opción."""
    consola.print("\n" + "=" * 50)
    consola.print("[bold cyan]📊 Sistema de Gestión de Matrículas[/bold cyan]")
    consola.print("=" * 50)
    consola.print("1. Gestionar Estudiantes")
    consola.print("2. Gestionar Cursos")
    consola.print("3. Gestionar Matrículas")
    consola.print("4. Ver Reportes")
    consola.print("5. Salir")

    opcion = Prompt.ask("[bold]Seleccione una opción[/bold]", choices=["1", "2", "3", "4", "5"], default="5")
    return opcion


def mostrar_menu_gestion(tipo: str) -> str:
    """Muestra un menú CRUD genérico para Estudiantes o Cursos."""
    consola.print(f"\n--- Gestión de {tipo} ---")
    consola.print(f"1. Crear {tipo}")
    consola.print(f"2. Listar {tipo}")
    consola.print(f"3. Actualizar {tipo}")
    consola.print(f"4. Eliminar {tipo}")
    consola.print("5. Volver al menú principal")

    opcion = Prompt.ask("[bold]Seleccione una opción[/bold]", choices=["1", "2", "3", "4", "5"], default="5")
    return opcion


def mostrar_menu_matriculas() -> str:
    """Muestra el menú de gestión de matrículas."""
    consola.print("\n--- Gestión de Matrículas ---")
    consola.print("1. Matricular estudiante en cursos")
    consola.print("2. Ver matrícula de un estudiante")
    consola.print("3. Volver al menú principal")

    opcion = Prompt.ask("[bold]Seleccione una opción[/bold]", choices=["1", "2", "3"], default="3")
    return opcion


def mostrar_menu_reportes() -> str:
    """Muestra el menú de reportes."""
    consola.print("\n--- Reportes ---")
    consola.print("1. Ver estudiantes por curso")
    consola.print("2. Calcular créditos de un estudiante (Reto Final)")
    consola.print("3. Volver al menú principal")

    opcion = Prompt.ask("[bold]Seleccione una opción[/bold]", choices=["1", "2", "3"], default="3")
    return opcion


def solicitar_datos_estudiante(actualizando: bool = False) -> dict:
    """Solicita los datos para crear o actualizar un estudiante."""
    id_estudiante = ""
    if not actualizando:
        id_estudiante = Prompt.ask("ID Estudiante (Ej. E001)")
    nombre = Prompt.ask("Nombre completo")
    carrera = Prompt.ask("Carrera")

    datos = {"nombre": nombre, "carrera": carrera}
    if not actualizando:
        datos["id_estudiante"] = id_estudiante
    return datos


def solicitar_datos_curso(actualizando: bool = False) -> dict:
    """Solicita los datos para crear o actualizar un curso."""
    id_curso = ""
    if not actualizando:
        id_curso = Prompt.ask("ID Curso (Ej. C001)")
    nombre_curso = Prompt.ask("Nombre del curso")
    # Usamos IntPrompt para validar que los créditos sean un número
    creditos = IntPrompt.ask("Créditos")

    datos = {"nombre_curso": nombre_curso, "creditos": creditos}
    if not actualizando:
        datos["id_curso"] = id_curso
    return datos


def solicitar_id(tipo: str) -> str:
    """Solicita un ID genérico."""
    return Prompt.ask(f"Ingrese el ID del {tipo}")


def solicitar_datos_matricula() -> dict:
    """Solicita los datos para una nueva matrícula."""
    id_estudiante = Prompt.ask("ID del Estudiante a matricular")
    periodo = Prompt.ask("Período académico (Ej. 2025-01)")

    id_cursos_str = Prompt.ask("IDs de los cursos (separados por coma, Ej. C001,C002)")
    id_cursos = [id_c.strip() for id_c in id_cursos_str.split(',')]

    return {"id_estudiante": id_estudiante, "periodo": periodo, "id_cursos": id_cursos}


def solicitar_periodo() -> str:
    """Solicita un período académico."""
    return Prompt.ask("Período académico (Ej. 2025-01)")


def mostrar_estudiantes(estudiantes: List[Estudiante]):
    """Muestra una lista de estudiantes en una tabla."""
    if not estudiantes:
        consola.print("[yellow]No hay estudiantes registrados.[/yellow]")
        return

    tabla = Table(title="Lista de Estudiantes")
    tabla.add_column("ID Estudiante", style="cyan", no_wrap=True)
    tabla.add_column("Nombre", style="magenta")
    tabla.add_column("Carrera", style="green")

    for est in estudiantes:
        tabla.add_row(est.id_estudiante, est.nombre, est.carrera)

    consola.print(tabla)


def mostrar_cursos(cursos: List[Curso]):
    """Muestra una lista de cursos en una tabla."""
    if not cursos:
        consola.print("[yellow]No hay cursos registrados.[/yellow]")
        return

    tabla = Table(title="Lista de Cursos")
    tabla.add_column("ID Curso", style="cyan", no_wrap=True)
    tabla.add_column("Nombre del Curso", style="magenta")
    tabla.add_column("Créditos", style="green", justify="right")

    for c in cursos:
        tabla.add_row(c.id_curso, c.nombre_curso, str(c.creditos))

    consola.print(tabla)


def mostrar_matricula_estudiante(estudiante: Estudiante, cursos: List[Curso], creditos_totales: int, periodo: str):
    """Muestra los cursos y créditos de un estudiante para un período."""

    panel_titulo = f"Matrícula de [bold]{estudiante.nombre}[/bold] ({estudiante.id_estudiante}) - Período: {periodo}"

    if not cursos:
        consola.print(Panel(f"El estudiante no tiene cursos matriculados en el período {periodo}.", title=panel_titulo,
                            border_style="yellow"))
        return

    tabla_cursos = Table(title="Cursos Matriculados")
    tabla_cursos.add_column("ID Curso", style="cyan")
    tabla_cursos.add_column("Nombre del Curso", style="magenta")
    tabla_cursos.add_column("Créditos", style="green", justify="right")

    for c in cursos:
        tabla_cursos.add_row(c.id_curso, c.nombre_curso, str(c.creditos))

    consola.print(Panel(tabla_cursos, title=panel_titulo, border_style="blue"))
    consola.print(f"[bold green]Total Créditos Matriculados: {creditos_totales}[/bold green]")


def mostrar_estudiantes_por_curso(curso: Curso, estudiantes: List[Estudiante]):
    """Muestra los estudiantes inscritos en un curso."""

    panel_titulo = f"Estudiantes en [bold]{curso.nombre_curso}[/bold] ({curso.id_curso})"

    if not estudiantes:
        consola.print(
            Panel("No hay estudiantes matriculados en este curso.", title=panel_titulo, border_style="yellow"))
        return

    tabla = Table(title="Lista de Estudiantes")
    tabla.add_column("ID Estudiante", style="cyan")
    tabla.add_column("Nombre", style="magenta")
    tabla.add_column("Carrera", style="green")

    for est in estudiantes:
        tabla.add_row(est.id_estudiante, est.nombre, est.carrera)

    consola.print(Panel(tabla, title=panel_titulo, border_style="blue"))


def pausar_pantalla():
    """Pausa la ejecución hasta que el usuario presione Enter."""
    Prompt.ask("\n[italic]Presione Enter para continuar...[/italic]")