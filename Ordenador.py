import os
import re
import shutil
from os.path import join

from exceptions_file import InvalidParameterTypeException


class Ordenador:
    ruta_actual = ""
    ruta_destino = ""
    carpetas_necesarias = {}
    patrones_compilados = {}

    def __init__(self, ruta_actual, ruta_destino, carpetas_necesarias):
        if not isinstance(ruta_actual, str):
            raise InvalidParameterTypeException("El primer parámetro debe ser una cadena de caracteres.")

        if not isinstance(ruta_destino, str):
            raise InvalidParameterTypeException("El segundo parámetro debe ser una cadena de caracteres.")

        if not isinstance(carpetas_necesarias, dict):
            raise InvalidParameterTypeException("El tercer parámetro debe ser un diccionario.")

        # ------------------ INICIALIZANDO VARIABLES ------------------
        self.ruta_actual = ruta_actual
        self.ruta_destino = ruta_destino
        self.carpetas_necesarias = carpetas_necesarias
        self.patrones_compilados = self.compilar_patrones(carpetas_necesarias)

    def compilar_patrones(self, carpetas_necesarias: dict):
        patrones = {}
        for carpeta, patron in carpetas_necesarias.items():
            if not isinstance(patron, str):
                raise InvalidParameterTypeException(
                    f'El patrón de la carpeta "{carpeta}" debe ser una cadena.'
                )

            try:
                patrones[carpeta] = re.compile(patron)
            except re.error as e:
                raise ValueError(
                    f'La expresión regular para la carpeta "{carpeta}" es inválida: {e}'
                ) from e

        return patrones

    def crear_carpetas_faltantes(self, carpetas_faltantes: list[str]):
        for faltante in carpetas_faltantes:
            try:
                os.makedirs(join(self.ruta_destino, faltante))
            except OSError as e:
                print(f"Error al crear el directorio: {faltante} -> {e}")
            else:
                print("Se creó con éxito: ", faltante)

    def pregunta(self):
        i = 0
        while (i := i + 1) <= 3:
            op = input("¿Desea agregar las carpetas faltantes? (s/n)\n\t-> ").strip().lower()
            if op == "s" or op == "n":
                return op

        return None

    def validar_ruta_de_destino(self):
        if not os.path.exists(self.ruta_destino):
            print(f'La ruta "{self.ruta_destino}" No existe')
            i = 0
            while (i := i + 1) <= 3:
                op = input(f"¿Desea crear la ruta {self.ruta_destino}? (s/n)\n\t-> ").strip().lower()
                if op == "n":
                    return False
                else:
                    os.makedirs(self.ruta_destino)
                    return True

            return False

        return True

    def revisar_carpetas_necesarias(self):
        carpetas_faltantes = [
            c
            for c in self.carpetas_necesarias
            if not os.path.exists(join(self.ruta_destino, c))
        ]
        if carpetas_faltantes:
            print("Faltan las carpetas:")
            for carpeta in carpetas_faltantes:
                print(f">> {carpeta}")

            respuesta = self.pregunta()
            if respuesta != "s":
                return False

            self.crear_carpetas_faltantes(carpetas_faltantes)

        return True

    def ordenar(self, archivo: str, nombre_del_archivo: str) -> None:
        for carpeta_destino, patron_compilado in self.patrones_compilados.items():
            if patron_compilado.fullmatch(nombre_del_archivo):
                try:
                    shutil.move(
                        join(self.ruta_actual, archivo),
                        join(self.ruta_destino, carpeta_destino),
                    )
                except OSError:
                    pass
                else:
                    print(f"Se movió el archivo: {archivo} a {carpeta_destino}")

    def start(self):
        if not self.validar_ruta_de_destino():
            return

        if not self.revisar_carpetas_necesarias():
            return

        archivos = [
            archivo
            for archivo in os.listdir(self.ruta_actual)
            if not archivo.startswith(".")
            and os.path.isfile(join(self.ruta_actual, archivo))
        ]

        if len(archivos) < 1:
            print("No hay archivos en la ruta especificada.")
            return

        for archivo in archivos:
            try:
                nombre_del_archivo = os.path.splitext(archivo)[0]
                self.ordenar(archivo, nombre_del_archivo)
            except OSError as e:
                print("Hubo un problema: ", e)
