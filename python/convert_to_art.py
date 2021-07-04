import sys
import os
import cv2
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(ROOT_DIR,"cycle_gan"))
from PIL import Image
from data import create_dataset
from models import create_model
from util import util
from data.base_dataset import get_transform
from set_default_args import TestOptions



def pic2art_cyclegan(image_path, filename):
    """Convert obtained image to an art style """
    image = Image.open(image_path).convert('RGB')
    opt = TestOptions().parse()  # get test options
    opt.num_threads = 0   # test code only supports num_threads = 0
    opt.batch_size = 1    # test code only supports batch_size = 1
    opt.serial_batches = True  # disable data shuffling; comment this line if results on randomly chosen images are needed.
    opt.no_flip = True    # no flip; comment this line if results on flipped images are needed.
    opt.display_id = -1   # no visdom display; the test code saves the results to a HTML file.

    model = create_model(opt)      # create a model given opt.model and other options
    model.setup(opt)               # regular setup: load and print networks; create schedulers

    # preprocess the input image
    input_nc = opt.output_nc if opt.direction == 'BtoA' else opt.input_nc
    transforms = get_transform(opt, grayscale=(input_nc == 1))
    img = transforms(image)
    img.unsqueeze_(0)
    image_dict = {'A':img, 'A_paths':['']}
#    for i, data in enumerate(dataset):
    model.set_input(image_dict)  # unpack data from data loader
    model.test()           # run inference
    visuals = model.get_current_visuals()  # get image results
    for label, im_data in visuals.items():
        if label=='fake':
            im = util.tensor2im(im_data)
            saved_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'processed_files', filename )
            cv2.imwrite(saved_path, cv2.cvtColor(im, cv2.COLOR_RGB2BGR))
            return saved_path
            

#            return im


#    
if __name__ == '__main__':
    import cv2
    import os
    image = cv2.imread('.\cycle_gan\datasets\park_photos\IMG-20210702-WA0004.jpg')
    A_path = '.\cycle_gan\datasets\park_photos\IMG-20210702-WA0004.jpg'
    dir_path = '.\data'
    files = os.listdir(dir_path)
    files_path = [os.path.join(dir_path, i) for i in files]
    for i in files_path:
        pic2art_cyclegan(i)