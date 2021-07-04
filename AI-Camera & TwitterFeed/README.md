# AI-CAMERA & TWITTER FEED DETECTION

This camera will automatically detect the animals and birds and captures the snapshots. It will avoid clicking picture when there are people around

## Important Files 
* `yolov3.cfg` file contains the network architecture used by YOLOv3 and placed it in the `/cfg/` folder. 
* `yolov3.weights` file contains the weights of pre-trained model and is placed in the `/weights/` directory. You can easily download the weights using the link https://pjreddie.com/darknet/yolo/
* `coco.names` file contains the list of the 80 object classes that the weights were trained to detect and is placed in the `/data/` directory.

# To Run the AI-Camera.
`python run_ai_smart_cam.py`

# To Run Twitter Feeds.
`python twitter_feeds.py`