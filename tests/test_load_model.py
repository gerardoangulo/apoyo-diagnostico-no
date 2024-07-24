import unittest
from unittest.mock import patch, MagicMock
import tensorflow as tf
from load_model import model  

class TestLoadModel(unittest.TestCase):

    @patch('load_model.tf.keras.models.load_model')
    def test_model_loading(self, mock_load_model):
        # Crear un modelo simulado
        mock_model = MagicMock()
        mock_load_model.return_value = mock_model

        # Llamar a la función de carga de modelo
        loaded_model = model()

        # Verificar que la función de carga de modelo fue llamada correctamente
        mock_load_model.assert_called_once_with('modelo_entrenado.h5')

        # Verificar que el modelo cargado es el esperado
        self.assertEqual(loaded_model, mock_model)

if __name__ == '__main__':
    unittest.main()
