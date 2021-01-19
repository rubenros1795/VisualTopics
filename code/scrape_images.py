import re, string
import numpy as np
import pandas as pd
from collections import Counter
import random
from tqdm import tqdm
import gensim
import os
from glob import glob as gb
import pickle,json
from matplotlib import pyplot as plt
import numpy as np
from functions import *
import concurrent.futures


with open('/media/ruben/OSDisk/Users/ruben.ros/Documents/GitHub/VisualTopicModelling/data/context-images.json','r') as f:
    dict_url = json.load(f)


smpl = random.sample(dict_url.keys(),2500)

dict_url = {k:v for k,v in dict_url.items() if k in smpl}

list_urls = []


for k,v in dict_url.items():

    for c,u in enumerate(v):
        fn = os.path.split(k)[-1].split('.')[0]
        fn = os.path.join('/media/ruben/OSDisk/Users/ruben.ros/Documents/GitHub/VisualTopicModelling/data/photos',fn)
        tpl = (fn + f"_{c}",u)
        
        list_urls.append(tpl)

print(f"Scraping {len(list_urls)} URLs")

with concurrent.futures.ThreadPoolExecutor() as e:
    for u in list_urls:
        e.submit(scrape, u)