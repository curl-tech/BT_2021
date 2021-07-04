import sys
# print(sys.argv[1])
import os
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(ROOT_DIR)
from convert_to_art import pic2art_cyclegan
# image_path = os.path.join(ROOT_DIR, 'uploaded_files', 'tmp-1-1625375036501')

# output_path = pic2art_cyclegan(image_path, 'art2332.png')
output_path = pic2art_cyclegan(sys.argv[1], sys.argv[2])
print(output_path)


