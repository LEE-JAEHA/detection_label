# when label shape => {"annotations":{"height":1512,"width":1512,"objects":[{"id":0,"class":13,"points":{"xtl":520,"ytl":608,"xbr":811,"ybr":991}}]}}


import os
import pandas as pd
from glob import glob
import shutil


label_path = '/DATA/02_bugdetection/labels'
image_path = '/DATA/02_bugdetection/images'
trg_path = '/USER/dataset/02_bugdetection_changed'
trg_path = '/USER/dataset/02_bugdetection_changed2'
# trg_path = '/USER/dataset/tmp'
modes = ['train', 'val', 'test']

if not os.path.isdir(trg_path): os.mkdir(trg_path)
if not os.path.isdir(os.path.join(trg_path, 'images')):
    print('copy images start')
    shutil.copytree(image_path, os.path.join(trg_path, 'images'))


if not os.path.isdir(os.path.join(trg_path, 'labels')): os.mkdir(os.path.join(trg_path, 'labels'))

for m in modes:
    print('convert', m , 'labels') 
    trg_path_mode = os.path.join(trg_path, 'labels', m)
    if not os.path.isdir(trg_path_mode): os.mkdir(trg_path_mode)
    json_list = glob(os.path.join(label_path, m, '*.json'))
    for json_path in json_list:
        label = pd.read_json(json_path)
        width = label.loc['width','annotations']
        height = label.loc['height','annotations']
        objects = label.loc['objects', 'annotations']
        f = open(os.path.join(trg_path_mode, json_path.split('/')[-1].split('.')[0] + '.txt'), 'w')
        # if len(objects) > 1:
        #     tmp = []
        #     import pdb;pdb.set_trace()
        for obj in objects:
            x_min, y_min, x_max, y_max = obj['points']['xtl'], obj['points']['ytl'], obj['points']['xbr'], obj['points']['ybr']
            if not (x_max <= width and y_max <= height):
                file = json_path.split('/')[-1].split('.')[0]
                print(f'invalid_size {x_max} > {width}, {y_max} > {height}, image name : {file}')
            clss = obj['class']
            data = f'{clss} {(x_min + x_max)/ (2 * width)} {(y_min + y_max)/ (2 * height)} {(x_max-x_min) / width} {(y_max-y_min) / height}\n'
            # if len(objects) > 1:
            #     tmp.append(data)
            #     import pdb;pdb.set_trace()
            f.write(data)
        f.close()

