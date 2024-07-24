import unittest
import read_img
import numpy as np
from PIL import Image

class TestReadImg(unittest.TestCase):
    def test_read_dicom_file(self):
        dicom_path = 'test-DICOM.dcm'
        img_RGB, img2show = read_img.read_dicom_file(dicom_path)
        
        self.assertIsInstance(img_RGB, np.ndarray)
        self.assertIsInstance(img2show, Image.Image)
    
    def test_read_jpg_file(self):
        jpg_path = 'test-JPG.jpg'
        img2, img2show = read_img.read_jpg_file(jpg_path)
        
        self.assertIsInstance(img2, np.ndarray)
        self.assertIsInstance(img2show, Image.Image)

if __name__ == '__main__':
    unittest.main()
