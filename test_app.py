import os
import unittest
from app import obtener_ultimos_datos_guardados, generar_pdf

class TestFunciones(unittest.TestCase):
    def test_obtener_ultimos_datos_guardados(self):
        # Crear un archivo CSV temporal con algunos datos
        archivo_temporal = 'C:/Users/Oscar/Desktop/cvs/datos_temporales.csv'
        with open(archivo_temporal, 'w') as file:
            file.write('Nombre,Edad\n')
            file.write('Juan,25\n')
            file.write('Maria,30\n')
        
        # Llamar a la función y verificar el resultado
        ultimos_datos = obtener_ultimos_datos_guardados(archivo_temporal)
        print(ultimos_datos)
        self.assertEqual(len(ultimos_datos), 1)
        self.assertEqual(ultimos_datos[0]['Nombre'], 'Maria')
        self.assertEqual(ultimos_datos[0]['Edad'], '30')
        

        # Eliminar el archivo temporal
        os.remove(archivo_temporal)

        # Definir los valores de prueba
    def test_generar_pdf(self):
        ruta_plantilla = "ruta/a/plantilla.pdf"
        diccionario = {"clave1": "valor1", "clave2": "valor2"}

        # Llamar a la función y verificar el resultado
        resultado = generar_pdf(ruta_plantilla)

        # Verificar que el nombre de la plantilla se reemplace correctamente
        self.assertNotIn("plantilla.pdf", resultado)
        self.assertIn("ruta/a/", resultado)
 
if __name__ == '__main__':
    unittest.main()