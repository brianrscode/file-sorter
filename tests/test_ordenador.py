import io
import os
import tempfile
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

from Ordenador import Ordenador
from exceptions_file import InvalidParameterTypeException


class TestOrdenador(unittest.TestCase):
    def test_init_raises_on_invalid_source_type(self):
        with self.assertRaises(InvalidParameterTypeException):
            Ordenador(123, "dest", {"IA": r"^x$"})

    def test_init_raises_on_invalid_regex(self):
        with self.assertRaises(ValueError):
            Ordenador("src", "dest", {"IA": "("})

    def test_ordenar_moves_matching_file(self):
        with (
            tempfile.TemporaryDirectory() as src_dir,
            tempfile.TemporaryDirectory() as dst_dir,
        ):
            os.makedirs(os.path.join(dst_dir, "IA"), exist_ok=True)
            file_name = "1.1 tarea_ApellidosNombre.txt"
            file_path = os.path.join(src_dir, file_name)

            with open(file_path, "w", encoding="utf-8") as f:
                f.write("content")

            reglas = {
                "IA": r"^\d+\.\d+\s[A-Za-zÀ-ÿ\s]+_ApellidosNombre$",
            }
            ordenador = Ordenador(src_dir, dst_dir, reglas)

            ordenador.ordenar(file_name, os.path.splitext(file_name)[0])

            self.assertFalse(os.path.exists(file_path))
            self.assertTrue(os.path.exists(os.path.join(dst_dir, "IA", file_name)))

    def test_ordenar_does_not_move_non_matching_file(self):
        with (
            tempfile.TemporaryDirectory() as src_dir,
            tempfile.TemporaryDirectory() as dst_dir,
        ):
            os.makedirs(os.path.join(dst_dir, "IA"), exist_ok=True)
            file_name = "archivo_sin_patron.txt"
            file_path = os.path.join(src_dir, file_name)

            with open(file_path, "w", encoding="utf-8") as f:
                f.write("content")

            reglas = {
                "IA": r"^\d+\.\d+\s[A-Za-zÀ-ÿ\s]+_ApellidosNombre$",
            }
            ordenador = Ordenador(src_dir, dst_dir, reglas)

            ordenador.ordenar(file_name, os.path.splitext(file_name)[0])

            self.assertTrue(os.path.exists(file_path))
            self.assertFalse(os.path.exists(os.path.join(dst_dir, "IA", file_name)))

    def test_revisar_carpetas_necesarias_respects_negative_answer(self):
        with (
            tempfile.TemporaryDirectory() as src_dir,
            tempfile.TemporaryDirectory() as dst_dir,
        ):
            reglas = {"IA": r"^x$"}
            ordenador = Ordenador(src_dir, dst_dir, reglas)

            with patch.object(Ordenador, "pregunta", return_value="n"):
                result = ordenador.revisar_carpetas_necesarias()

            self.assertFalse(result)
            self.assertFalse(os.path.exists(os.path.join(dst_dir, "IA")))

    def test_start_with_empty_source_prints_message(self):
        with (
            tempfile.TemporaryDirectory() as src_dir,
            tempfile.TemporaryDirectory() as dst_dir,
        ):
            os.makedirs(os.path.join(dst_dir, "IA"), exist_ok=True)
            reglas = {"IA": r"^x$"}
            ordenador = Ordenador(src_dir, dst_dir, reglas)

            output = io.StringIO()
            with redirect_stdout(output):
                ordenador.start()

            self.assertIn("No hay archivos en la ruta especificada.", output.getvalue())


if __name__ == "__main__":
    unittest.main()
