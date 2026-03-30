"""
Este código al ejecutarse sobre cualquier directorio buscará ciertos patrones dados con regex
en los archivos del directorio y si hay alguna coincidencia se moveran a la carpeta destino
en la cual hay varias subcarpetas para agrupar los archivos de acuerdo a los patrones encontrados
"""

import os
from banners import getBanner
from Ordenador import Ordenador

ruta_actual = os.path.join(os.getcwd(), "")  # Ruta en la que se encuentra el usuario

home_path = os.path.expanduser("~")  # HOME de usuario
ruta_destino = os.path.join(home_path, "Escuela")  # ruta en la que hará el ordenamiento

# Subcarpetas del directorio y lo patrones que almacenará
carpetas = {
    # 4.2-ApaternoAmaternoNombreTablaDescriptiva
    "IA": r"^\d+\.\d+\s[A-Za-zÀ-ÿ\s]+_ApellidosNombre$",
    "investigacion": r"^\d+\.\d+-ApellidoosNombre[A-Za-zÀ-ÿ\s]+$",
    "proceso_p": r"^\d+\.\d+\s[A-Za-zÀ-ÿ\s]+-Apellido Nombre$",
    "web": r"^Actividad\s\d+_Apellido\sNombre_web$",
}


if __name__ == "__main__":
    ordena = Ordenador(ruta_actual, ruta_destino, carpetas)
    print(getBanner())
    # while True:
    #     time.sleep(5)
    #     ordena.start()
    ordena.start()
