import zipfile
import os
import pandas as pd
import shutil
from main import analysis


def create_results(numid):

    #create results folder
    if not os.path.exists('uploads/result'):
        os.makedirs('uploads/result')
    else:
        shutil.rmtree('uploads/result')
        os.makedirs('uploads/result')

    filepath = 'uploads/export/apple_health_export/electrocardiograms'

    with zipfile.ZipFile('uploads/export.zip', 'r') as f:
        files = [n for n in f.namelist() if n.startswith('apple_health_export/electrocardiograms/') and not n.endswith('/')]
        f.extractall(path='uploads/export/' , members=files)

    filename=os.listdir(filepath)

    index = (-1-int(numid))

    analysis(filename[index], filepath, save_folder='uploads/result', save_svg=True)

    #create result zip
    shutil.make_archive('uploads/result', 'zip', 'uploads/result')