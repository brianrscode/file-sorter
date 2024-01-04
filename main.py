import os
from banners import getBanner
from Ordenador import Ordenador

ruta_actual = os.path.join(os.getcwd(), "")
ruta_destino = "/home/lnxp/Escuela/"  # ruta sobre la que se ejecutará el script

carpetas = {
    "Estructuras": r"\d+\.\d+\s[a-zA-zÀ-ú\s]+-Apellido Nombre",
    "Calculo": r"Actividad\s\d+_Apellido\sNombre_CVectorial",
}


if __name__ == "__main__":
    ordena = Ordenador(ruta_actual, ruta_destino, carpetas)
    print(getBanner())
    # while True:
    #     time.sleep(5)
    #     ordena.start()
    ordena.start()
