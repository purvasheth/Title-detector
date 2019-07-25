import sys
import argparse
from yolo import YOLO
from PIL import Image
import os
import json


if len (sys.argv) != 2 :
    print("Usage: python yolo_image.py folder_path")
    sys.exit(1)
folder_path = sys.argv[1]
data = {}
for img in os.listdir(folder_path):
    try:
        print("Processing image:",img)
        image = Image.open(folder_path + "/"+ img)
    except:
        print('Open Error! Try again! for' + img)
    else:
        yolo = YOLO()
        r_image = yolo.detect_image(image,img,data)
        r_image.save("prediction/"+img,"JPEG")
yolo.close_session()
with open("intermediate.json", "w") as write_file:
    json.dump(data, write_file)
