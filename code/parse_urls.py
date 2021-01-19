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

df = pd.read_csv('/home/ruben/Documents/TankMan/data/original/TankMan.tsv',sep='\t')
ids = dict(zip(df['uuid'],df['page_url']))

data = {}

for u in tqdm(gb('/home/ruben/Documents/TankMan/data/html/*.html')):
    url = ids[os.path.split(u)[-1].split('.')[0]]
    tags = findtags(url,u)
    if tags:
        data.update({u:tags})

with open('/media/ruben/OSDisk/Users/ruben.ros/Documents/GitHub/VisualTopicModelling/data/context-images.json','w') as f:
    json.dump(data,f)