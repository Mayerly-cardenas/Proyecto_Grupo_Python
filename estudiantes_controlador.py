from __future__ import annotations
import json
from typing import List, Dict, Any
from rich.console import Console

console = Console()
DATA_FILE = "data/estudiantes.json"


class EstudianteController:
    """Controlador que maneja las operaciones CRUD sobre los estudiantes."""

    def __init__(self) -> None:
        """Inicializa el controlador y carga los datos del archivo JSON."""
        self.estudiantes: List[Dict[str, Any]] = self._cargar_datos()

    @staticmethod
    def _cargar_datos() -> List[Dict[str, Any]]:
        """
        Carga los datos de los estudiantes desde el archivo JSON.

        Returns:
            List[Dict[str, Any]]: Lista de estudiantes.
        """
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as archivo:
                return json.load(archivo)
        except FileNotFoundError:
            console.print("[yellow]Archivo no encontrado, creando nuevo archivo...[/yellow]")
            return []
        except json.JSONDecodeError:
            console.print("[red]Error al leer el archivo JSON. Verifica su formato.[/red]")
            return []

    def _guardar_datos(self) -> None:
        """Guarda los datos actuales en el archivo JSON."""
        try:
            with open(DATA_FILE, "w", encoding="utf-8") as archivo:
                json.dump(self.estudiantes, archivo, indent=4, ensure_ascii=False)
            console.print("[green]Datos guardados correctamente.[/green]")
        except Exception as e:
            console.print(f"[red]Error al guardar los datos: {e}[/red]")

    def crear_estudiante(self, nombre: str, edad: int, programa: str) -> None:
        """Crea un nuevo estudiante."""
        nuevo = {"nombre": nombre, "edad": edad, "programa": programa}
        self.estudiantes.append(nuevo)
        self._guardar_datos()
        console.print(f"[green]Estudiante {nombre} agregado correctamente.[/green]")

    def listar_estudiantes(self) -> None:
        """Muestra la lista de estudiantes."""
        if not self.estudiantes:
            console.print("[yellow]No hay estudiantes registrados.[/yellow]")
            return
        for i, est in enumerate(self.estudiantes, start=1):
            console.print(f"{i}. {est['nombre']} - {est['programa']} ({est['edad']} años)")

    def actualizar_estudiante(self, nombre: str, nuevo_programa: str) -> None:
        """Actualiza el programa de un estudiante."""
        for est in self.estudiantes:
            if est["nombre"].lower() == nombre.lower():
                est["programa"] = nuevo_programa
                self._guardar_datos()
                console.print(f"[green]Programa de {nombre} actualizado correctamente.[/green]")
                return
        console.print(f"[red]No se encontró al estudiante {nombre}.[/red]")

    def eliminar_estudiante(self, nombre: str) -> None:
        """Elimina un estudiante por nombre."""
        for est in self.estudiantes:
            if est["nombre"].lower() == nombre.lower():
                self.estudiantes.remove(est)
                self._guardar_datos()
                console.print(f"[green]Estudiante {nombre} eliminado.[/green]")
                return
        console.print(f"[red]No se encontró al estudiante {nombre}.[/red]")
