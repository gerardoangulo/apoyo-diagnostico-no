import unittest
import numpy as np
import cv2
from preprocess_img import preprocess  # Ajusta la ruta según tu estructura de proyecto

class TestPreprocessImg(unittest.TestCase):

    def setUp(self):
        # Crear un array de prueba (por ejemplo, una imagen de 256x256 con valores en escala de grises)
        self.sample_array = np.random.randint(0, 256, (256, 256, 3), dtype=np.uint8)

    def test_preprocess_success(self):
        processed_array = preprocess(self.sample_array)
        
        # Verificar las dimensiones del array procesado
        self.assertEqual(processed_array.shape, (1, 512, 512, 1))
        
        # Verificar el tipo de datos del array procesado
        self.assertEqual(processed_array.dtype, np.float64)
        
        # Verificar que los valores están normalizados entre 0 y 1
        self.assertTrue(np.all(processed_array >= 0.0) and np.all(processed_array <= 1.0))

    def test_preprocess_invalid_input(self):
        with self.assertRaises(cv2.error):
            preprocess("invalid input")

if __name__ == '__main__':
    unittest.main()
