import os 
from glob import glob as gb
from tqdm import tqdm
from collections import Counter

photos = gb('/media/ruben/OSDisk/Users/ruben.ros/Documents/GitHub/VisualTopicModelling/data/photos/*')

# for photo in tqdm(photos):
#     size = os.path.getsize(photo)
#     if size / 1000 < 10:
#         os.remove(photo)
