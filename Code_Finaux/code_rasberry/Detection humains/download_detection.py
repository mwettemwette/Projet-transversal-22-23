import os
import gdown

if (not os.path.isfile("yolov3-tiny.cfg")):
    gdown.download("https://drive.google.com/u/3/uc?id=1jc6iuRn8X5qcF5UIVKue6AJQRXbjk-2_&export=download", "yolov3-tiny.cfg", quiet=True)
else:(print("yolov3-tiny.cfg present"))

if (not os.path.isfile("yolov3-tiny.weights")):
    gdown.download("https://drive.google.com/u/3/uc?id=1TTy6xph7E7L2uaSv6olUOkEDamI6TtR6&export=download", "yolov3-tiny.weights", quiet=True)
else:(print("yolov3-tiny.weights present"))    
    
if (not os.path.isfile("coco.names")):
    gdown.download("https://drive.google.com/u/3/uc?id=1ckTVwxy_r6uLLAkNQmoouHf4O08NIQcZ&export=download", "coco.names", quiet=True)
else:(print("coco.names present"))