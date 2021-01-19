from imagededup.methods import PHash
from collections import Counter
import pandas as pd
import shutil
import os
phasher = PHash()


input_folder = '/media/ruben/OSDisk/Users/ruben.ros/Documents/GitHub/VisualTopicModelling/data/photos/'

######

def Cluster(input_folder):

    img_files = [i for i in os.listdir(input_folder) if ".txt" not in i]

    img_folder = os.path.join(input_folder,"img")

    if not os.path.exists(img_folder):
        os.makedirs(img_folder)

    for im in img_files:
        old_fn = os.path.join(input_folder,im)
        new_fn = os.path.join(img_folder,im)
        shutil.move(old_fn, new_fn)

    # Generate encodings for all images in an image directory
    encodings = phasher.encode_images(image_dir=img_folder)

    # Find duplicates using the generated encodings
    duplicates = phasher.find_duplicates(encoding_map=encodings)
    df = []
    for k,v in duplicates.items():
        if len(v) > 0:
            for it in v:
                df.append([k,it])
        elif len(v) == 0:
            df.append([k,k])
        else:
            continue
    df = pd.DataFrame(df,columns=['a','b'])

    # Transform Duplicate Pairs to Clusters
    def consolidate(sets):
        # http://rosettacode.org/wiki/Set_consolidation#Python:_Iterative
        setlist = [s for s in sets if s]
        for i, s1 in enumerate(setlist):
            if s1:
                for s2 in setlist[i+1:]:
                    intersection = s1.intersection(s2)
                    if intersection:
                        s2.update(s1)
                        s1.clear()
                        s1 = s2
        return [s for s in setlist if s]

    def group_ids(pairs):
        groups = consolidate(map(set, pairs))
        d = {}
        for i, group in enumerate(sorted(groups)):
            for elem in group:
                d[elem] = i
        return d

    df['c'] = df['a'].replace(group_ids(zip(df.a,df.b)))
    print("INFO: {} clusters found".format(len(set(df['c']))))

    # Renaming Files
    single = 0
    multiple = 0

    newfilenames = []
    for i in set(df['c']):
        tmp = df[df['c'] == i]
        tmp = list(set(list(tmp['a']) + list(tmp['b'])))
        if len(tmp) == 1:
            single += 1
            for fn in tmp:
                newfn = "cluster_single_{}_{}".format(i,fn)
                newfilenames.append(newfn)
                newfn = os.path.join(img_folder,newfn)
                oldfn = os.path.join(img_folder,fn)
                os.rename(oldfn,newfn)
        if len(tmp) > 1:
            multiple += 1
            for fn in tmp:
                newfn = "cluster_{}_{}".format(i,fn)
                newfilenames.append(newfn)
                newfn = os.path.join(img_folder,newfn)
                oldfn = os.path.join(img_folder,fn)
                os.rename(oldfn,newfn)


    image_files = newfilenames

    for im in image_files:
        old_fn = os.path.join(img_folder,im)
        new_fn = os.path.join(input_folder,im)
        shutil.move(old_fn, new_fn)

    os.rmdir(img_folder)
    print('INFO: renamed files.')
    print('---- There are {} clusters that have only one image'.format(single))
    print('---- You can now manually select relevant images in {}'.format(input_folder))


####

if __name__ == '__main__':
    Cluster(input_folder)
