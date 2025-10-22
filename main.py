# main.py
import sys
from vista import consola as vista
from controlador import estudiantes_ctrl, cursos_ctrl, matriculas_ctrl


def gestionar_estudiantes():
    """Maneja el submenú de gestión de estudiantes."""
    while True:
        opcion = vista.mostrar_menu_gestion("Estudiante")

        try:
            if opcion == "1":  # Crear
                datos = vista.solicitar_datos_estudiante()
                estudiantes_ctrl.crear_estudiante(**datos)
                vista.mostrar_exito("Estudiante creado correctamente.")

            elif opcion == "2":  # Listar
                estudiantes = estudiantes_ctrl.obtener_estudiantes()
                vista.mostrar_estudiantes(estudiantes)

            elif opcion == "3":  # Actualizar
                id_est = vista.solicitar_id("estudiante a actualizar")
                estudiante = estudiantes_ctrl.obtener_estudiante_por_id(id_est)
                if estudiante:
                    vista.consola.print(f"Actualizando a: {estudiante.nombre}")
                    datos = vista.solicitar_datos_estudiante(actualizando=True)
                    estudiantes_ctrl.actualizar_estudiante(id_est, **datos)
                    vista.mostrar_exito("Estudiante actualizado.")
                else:
                    vista.mostrar_error("Estudiante no encontrado.")

            elif opcion == "4":  # Eliminar
                id_est = vista.solicitar_id("estudiante a eliminar")
                estudiantes_ctrl.eliminar_estudiante(id_est)
                vista.mostrar_exito("Estudiante eliminado.")

            elif opcion == "5":  # Volver
                break

        except ValueError as e:
            vista.mostrar_error(str(e))
        except Exception as e:
            vista.mostrar_error(f"Ocurrió un error inesperado: {e}")

        if opcion != "2":  # No pausar después de listar
            vista.pausar_pantalla()


def gestionar_cursos():
    """Maneja el submenú de gestión de cursos."""
    while True:
        opcion = vista.mostrar_menu_gestion("Curso")

        try:
            if opcion == "1":  # Crear
                datos = vista.solicitar_datos_curso()
                cursos_ctrl.crear_curso(**datos)
                vista.mostrar_exito("Curso creado correctamente.")

            elif opcion == "2":  # Listar
                cursos = cursos_ctrl.obtener_cursos()
                vista.mostrar_cursos(cursos)

            elif opcion == "3":  # Actualizar
                id_curso = vista.solicitar_id("curso a actualizar")
                curso = cursos_ctrl.obtener_curso_por_id(id_curso)
                if curso:
                    vista.consola.print(f"Actualizando a: {curso.nombre_curso}")
                    datos = vista.solicitar_datos_curso(actualizando=True)
                    cursos_ctrl.actualizar_curso(id_curso, **datos)
                    vista.mostrar_exito("Curso actualizado.")
                else:
                    vista.mostrar_error("Curso no encontrado.")

            elif opcion == "4":  # Eliminar
                id_curso = vista.solicitar_id("curso a eliminar")
                cursos_ctrl.eliminar_curso(id_curso)
                vista.mostrar_exito("Curso eliminado.")

            elif opcion == "5":  # Volver
                break

        except ValueError as e:
            vista.mostrar_error(str(e))
        except Exception as e:
            vista.mostrar_error(f"Ocurrió un error inesperado: {e}")

        if opcion != "2":
            vista.pausar_pantalla()


def gestionar_matriculas():
    """Maneja el submenú de matrículas."""
    while True:
        opcion = vista.mostrar_menu_matriculas()

        try:
            if opcion == "1":  # Matricular
                datos = vista.solicitar_datos_matricula()
                matriculas_ctrl.matricular_estudiante(
                    datos["id_estudiante"],
                    datos["id_cursos"],
                    datos["periodo"]
                )
                vista.mostrar_exito("Estudiante matriculado exitosamente.")

            elif opcion == "2":  # Ver matrícula de estudiante
                id_est = vista.solicitar_id("estudiante")
                periodo = vista.solicitar_periodo()
                estudiante = estudiantes_ctrl.obtener_estudiante_por_id(id_est)

                if not estudiante:
                    vista.mostrar_error("Estudiante no encontrado.")
                    continue

                matriculas = matriculas_ctrl.obtener_matriculas_por_estudiante(id_est)
                matricula_periodo = None
                for m in matriculas:
                    if m.periodo_academico == periodo:
                        matricula_periodo = m
                        break

                cursos_matriculados = []
                creditos_totales = 0
                if matricula_periodo:
                    for id_c in matricula_periodo.id_cursos:
                        curso = cursos_ctrl.obtener_curso_por_id(id_c)
                        if curso:
                            cursos_matriculados.append(curso)

                    creditos_totales = matriculas_ctrl.calcular_creditos_estudiante(id_est, periodo)

                vista.mostrar_matricula_estudiante(estudiante, cursos_matriculados, creditos_totales, periodo)

            elif opcion == "3":  # Volver
                break

        except ValueError as e:
            vista.mostrar_error(str(e))
        except Exception as e:
            vista.mostrar_error(f"Ocurrió un error inesperado: {e}")

        vista.pausar_pantalla()


def gestionar_reportes():
    """Maneja el submenú de reportes."""
    while True:
        opcion = vista.mostrar_menu_reportes()

        try:
            if opcion == "1":  # Estudiantes por curso
                id_curso = vista.solicitar_id("curso")
                curso = cursos_ctrl.obtener_curso_por_id(id_curso)

                if not curso:
                    vista.mostrar_error("Curso no encontrado.")
                    continue

                estudiantes = matriculas_ctrl.obtener_estudiantes_por_curso(id_curso)
                vista.mostrar_estudiantes_por_curso(curso, estudiantes)

            elif opcion == "2":  # Calcular créditos (Reto Final)
                id_est = vista.solicitar_id("estudiante")
                periodo = vista.solicitar_periodo()

                estudiante = estudiantes_ctrl.obtener_estudiante_por_id(id_est)
                if not estudiante:
                    vista.mostrar_error("Estudiante no encontrado.")
                    continue

                creditos = matriculas_ctrl.calcular_creditos_estudiante(id_est, periodo)
                vista.mostrar_exito(
                    f"El estudiante [bold]{estudiante.nombre}[/bold] tiene [bold]{creditos}[/bold] créditos en el período {periodo}.")

            elif opcion == "3":  # Volver
                break

        except ValueError as e:
            vista.mostrar_error(str(e))
        except Exception as e:
            vista.mostrar_error(f"Ocurrió un error inesperado: {e}")

        vista.pausar_pantalla()


def main():
    """Función principal de la aplicación."""
    while True:
        opcion = vista.mostrar_menu_principal()

        if opcion == "1":
            gestionar_estudiantes()
        elif opcion == "2":
            gestionar_cursos()
        elif opcion == "3":
            gestionar_matriculas()
        elif opcion == "4":
            gestionar_reportes()
        elif opcion == "5":
            vista.consola.print("[bold green]¡Hasta luego! 👋[/bold green]")
            sys.exit(0)


if __name__ == "__main__":
    main()