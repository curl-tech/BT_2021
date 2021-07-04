import sys
print(sys.argv[1])
import os
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(ROOT_DIR)
from convert_to_art import pic2art_cyclegan
print("after convert")
image_path = os.path.join(ROOT_DIR, 'uploaded_files', 'img_0')

output_path = pic2art_cyclegan(image_path, 'art.png')


