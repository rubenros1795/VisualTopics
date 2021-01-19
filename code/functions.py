from bs4 import BeautifulSoup
import datetime, csv
import pandas as pd
import requests
import string
import re as regexz
import random
from tqdm import tqdm
import json
import os
import time
import uuid
import concurrent.futures
from nltk.tokenize import word_tokenize
import spacy
import codecs
import math
import shutil
from PIL import Image
import io
from urllib.parse import urlparse
import tldextract

def findtags(page_url,filename):

        # Find Image Files in Html
        
        with codecs.open(filename,'r',encoding='utf-8',errors='ignore') as f:
            html_object = f.read()
        soup = BeautifulSoup(html_object, "html.parser")
        image_tags = []
        for tag in ['img','meta','a']:
            tt = soup.findAll(tag)
            image_tags += tt
        
        list_url = []
        extensions = ".jpg .JPG .JPEG .jpeg .Jpeg .png".split(' ')
        for c,tag in enumerate(image_tags):
            attributes = dict(tag.attrs)

            for k,v in attributes.items():
                # Extract Image
                if any(substring in v for substring in extensions) and "logo" not in v and "icon" not in v:

                    list_url.append(v)

        # Normalize URLs pasted together
        commas = [tpl for sublist in [i.split(',') for i in list_url if "," in i] for tpl in sublist]
        imgs = list(set(list_url + commas))

        correct = [i for i in imgs if "?w" not in i]
        potentials = [i.split("?w") for i in imgs if "?w" in i]

        for pbase in list(set([i[0] for i in potentials])):
            all_p = [i for i in potentials if i[0] == pbase]
            pdef = "?w".join(all_p[0])
            if "," in pdef:
                [correct.append(i) for i in pdef.split(',')]
            else:
                correct.append(pdef)
        list_url = correct

        # Append urls without tld
        tld = ".".join(tldextract.extract(page_url))
        list_url = [u for u in list_url if u]
        if len(list_url) == 0 or list_url == None:
            return 
        list_http = [x for x in list_url if x[:4] == "http"]
        list_incomplete = [tld + x for x in list_url if x[0] == "/"]
        
        list_url = list_http + list_incomplete
        list_url = [u for u in list_url if u]
        
        # list_correct = []

        # for u in list_url:
        #     n = u[0].split(u[1])[0] + u[1]
        #     list_correct.append(n)
        
        if len(list_url) > 0:
            return list_url
        else:
            return

def scrape(tpl):
        fn = tpl[0]
        url = tpl[1]

        if "png" in url:
            fn = str(fn) + ".png"
        elif "jpg" in url:
            fn = str(fn) + ".jpg"
        elif "Jpeg" in url:
            fn = str(fn) + ".jpg"
        elif "jpeg" in url:
            fn = str(fn) + ".jpg"
        elif "JPG" in url:
            fn = str(fn) + ".jpg"
        else:
            return 

        try:
            image_content = requests.get(url, timeout=20,stream=True).content
            image_file = io.BytesIO(image_content)
            image = Image.open(image_file).convert('RGB')
            with open(fn, 'wb') as f:
                image.save(f)

            del image

        except Exception as e:
            return