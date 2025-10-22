from rich.console import Console
from rich.panel import Panel
from estudiantes_controlador import EstudianteController

console = Console()


def menu_principal() -> None:
    """Muestra el menú principal y gestiona las opciones."""
    controlador = EstudianteController()

    while True:
        console.print(Panel("[bold cyan]Menú Principal[/bold cyan]\n"
                            "1. Crear estudiante\n"
                            "2. Listar estudiantes\n"
                            "3. Actualizar estudiante\n"
                            "4. Eliminar estudiante\n"
                            "5. Salir",
                            title="Sistema de Gestión SENA",
                            subtitle="Control de estudiantes"))

        opcion = console.input("[yellow]Seleccione una opción: [/yellow]")

        try:
            if opcion == "1":
                nombre = console.input("Nombre: ")
                edad = int(console.input("Edad: "))
                programa = console.input("Programa: ")
                controlador.crear_estudiante(nombre, edad, programa)

            elif opcion == "2":
                controlador.listar_estudiantes()

            elif opcion == "3":
                nombre = console.input("Nombre del estudiante a actualizar: ")
                nuevo_prog = console.input("Nuevo programa: ")
                controlador.actualizar_estudiante(nombre, nuevo_prog)

            elif opcion == "4":
                nombre = console.input("Nombre del estudiante a eliminar: ")
                controlador.eliminar_estudiante(nombre)

            elif opcion == "5":
                console.print("[bold green]Saliendo del sistema...[/bold green]")
                break

            else:
                console.print("[red]Opción no válida.[/red]")

        except ValueError:
            console.print("[red]Error: Ingrese valores válidos.[/red]")


if __name__ == "__main__":
    menu_principal()
