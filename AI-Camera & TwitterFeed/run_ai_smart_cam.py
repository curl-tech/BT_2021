import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
# importing the requests library
import requests

from utils import load_class_names,detect_objects,print_objects
from darknet import Darknet

# Set the NMS threshold
nms_thresh = 0.6
# Set the IOU threshold
iou_thresh = 0.4

cfg_file = './cfg/yolov3.cfg'# Set the location and name of the cfg file
weight_file = './weights/yolov3.weights' # Set the location and name of the pre-trained weights file
namesfile = 'data/coco.names'# Set the location and name of the COCO object classes file


def plot_boxes_videos(img, boxes, class_names, plot_labels, color = None):

    red = (0,0,255)
    green = (0,255,0)
    
    # Get the width and height of the image
    width = img.shape[1]
    height = img.shape[0]
    
    # Plot the bounding boxes and corresponding labels on top of the image
    for i in range(len(boxes)):
        # Get the ith bounding box
        box = boxes[i]
        # Get the (x,y) pixel coordinates of the lower-left and lower-right corners
        # of the bounding box relative to the size of the image. 
        x1 = int(np.around((box[0] - box[2]/2.0) * width))
        y1 = int(np.around((box[1] - box[3]/2.0) * height))
        x2 = int(np.around((box[0] + box[2]/2.0) * width))
        y2 = int(np.around((box[1] + box[3]/2.0) * height))
        # Calculate the width and height of the bounding box relative to the size of the image.
        width_x = x2 - x1
        width_y = y1 - y2
        # Use the same color to plot the bounding boxes of the same object class
        if len(box) >= 7 and class_names:
            cls_conf = box[5]
            cls_id = box[6]
            
        #ignores 'sports ball'
        if cls_id == 32:
            continue
       
        # Set the default rgb value to green
        color = green
        if cls_id == 0: #red color for person
            color = red
    
        #drawing the rectangle around the faces
        cv2.rectangle(img,(x1, y2),(x1+width_x, y2+width_y),color,2)
        
        # If plot_labels = True then plot the corresponding label
        if plot_labels:
            # Create a string with the object class name and the corresponding object class probability
            if cls_id in list(range(15,24)):
                conf_tx = "Animal" + ': {:.1f}'.format(cls_conf)
            else:
                conf_tx = class_names[cls_id] + ': {:.1f}'.format(cls_conf)
            # conf_tx = class_names[cls_id] + ': {:.1f}'.format(cls_conf)
            
            # Define x and y offsets for the labels
            lxc = int((img.shape[1] * 0.266) / 100)
            lyc = int((img.shape[0] * 1.180) / 100)

            #mask or no mask text
            cv2.putText(img, conf_tx, (x1 + lxc, y1 - lyc),cv2.FONT_HERSHEY_SIMPLEX,1,color,2)

def capture_snapshots(img,img_org, boxes, class_names,prev_id = None,prev_conf = None,count = 0):
    is_person = False
    max_count = 1
    red = (0,0,255)
    green = (0,255,0)
    #check for person in the image frames
    for box in boxes:
        if box[6] == 0:
            is_person = True
            break
    if is_person:
        cv2.putText(img,"Not Capturing" , (10, 25),cv2.FONT_HERSHEY_SIMPLEX,1,red,2)
        return 0,0,0
    
    #take the first box
    box = boxes[0]
    cls_conf = box[5]
    cls_id = box[6]
    
    #small function
    def save_img(img,count,cls_conf):
        count += 1
        cv2.putText(img,f"Capturing Image" , (10, 25),cv2.FONT_HERSHEY_SIMPLEX,1,green,2) # {count} {cls_conf}
        num = len(os.listdir('output_imgs'))
        cv2.imwrite(f"output_imgs/img_{num}.png",img_org)
        return cls_id, cls_conf, count
    
    if cls_conf>0.9:
        if cls_id != prev_id:
            return save_img(img,count,cls_conf)
        elif cls_id == prev_id and count<max_count and cls_conf!=prev_conf:
            return save_img(img,count,cls_conf)
        else:
            return prev_id, prev_conf, count
    else:
        return prev_id,prev_conf,count

def remove_old_files():
    rem_dir = "output_imgs"
    fns = list(os.listdir(rem_dir))
    for fn in fns:
        os.remove(os.path.join(rem_dir,fn))
        print(f"Removed: {fn}")

def post_snapshots():
    # defining the api-endpoint 
    URL = "http://localhost:8080/nature/upload-file"
    # file = cv2.imread("output_imgs/img_0.png")
    img_dir = "output_imgs"
    file_names = os.listdir(img_dir)
    for idx, fn in enumerate(file_names):
        files = {'file': open(os.path.join(img_dir,fn), 'rb')}
        data = {
            "artName":f"AiArt_{idx}",
            "artDescription":"Coming From AI Camera"
        }
        print(f"Posting images {idx+1}/{len(file_names)}")
        r = requests.post(URL, files=files, data=data)
        print("image uploaded....!")
        break    

def run_ai_camera(path_to_video = "Final_2.mp4"):
    #Remove the previous imgs
    remove_old_files()
    # Load the network architecture
    model = Darknet(cfg_file)
    # Load the pre-trained weights
    model.load_weights(weight_file)
    # Load the COCO object classes from utils.py
    class_names = load_class_names(namesfile)

    #initialize video obj
    cap = cv2.VideoCapture(path_to_video)
    last_frame_num = cap.get(cv2.CAP_PROP_FRAME_COUNT)

    #some initializations
    prev_id = None
    prev_conf = None
    count = 0
    frame_count = 0
    counter = 0
    #reading and capturing all the frames
    while(True):
        #reading the image frames
        ret,img = cap.read()
        counter += 1
        frame_count += 1
        if counter%9 ==0:
            # Convert the image to RGB
            # img_org = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img_org = img.copy()

            # We resize the image to the input width and height of the first layer of the network.    
            img_resize = cv2.resize(img_org, (model.width, model.height))

            # Detect objects in the image
            boxes = detect_objects(model, img_resize, iou_thresh, nms_thresh)
            
            # plots the bbox around objects
            plot_boxes_videos(img, boxes, class_names, plot_labels = True) #,color = (0,0,255)
            
            #capture the frames
            if len(boxes)>0:
                prev_id,prev_conf,count = capture_snapshots(img,img_org, boxes, class_names,prev_id = prev_id, prev_conf = prev_conf,count = count)
            
            cv2.imshow('LIVE',img)
            key = cv2.waitKey(1)
            
            #break if escape key is pressed
            if key == 27:
                break
        #Check if video is ended
        if frame_count >= last_frame_num:
            print("Video Ended")
            break
        
    #destroy all the windows
    cv2.destroyAllWindows()
    cap.release()

if __name__ == '__main__':
    path_to_video = "Final.mp4"
    run_ai_camera(path_to_video)
    post_snapshots()