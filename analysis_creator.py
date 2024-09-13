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

    with zipfile.ZipFile('uploads/export.zip') as myzip:
        myzip.extractall('uploads/export')
        filename=os.listdir('uploads/export/apple_health_export/electrocardiograms')

    df = pd.read_csv('uploads/export/apple_health_export/electrocardiograms/'+filename[-1])

    filepath = 'uploads/export/apple_health_export/electrocardiograms'

    index = (-1-int(numid))

    analysis(filename[index], filepath, save_folder='uploads/result', save_svg=True)

    #create result zip
    shutil.make_archive('uploads/result', 'zip', 'uploads/result')