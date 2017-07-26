from keras.preprocessing import image
import cv2
import numpy as np
from matplotlib import pyplot as plt
import glob
import sys
import os
import numpy as np
from lib.resnet50 import ResNet50
from lib.imagenet_utils import preprocess_input
from keras.models import Model
from src import layer_extraction
from src import preprocessing


os.getcwd()
chdir('/Users/Walkon302/Google Drive/CDIPS_Recommender')

def file_loader(folder_path, file_type):
    '''
    Parameters:
    -----------
    folder_path: str
        path of the input folder
    file_type: str
        type of files of interest

    Return:
    -------
    file_list: list
        List of absolute path of files within input folder
    '''
    curwd = os.getcwd()
    ab_path = curwd + '/' + folder_path
    folder = '{}/*.{}'.format(ab_path, file_type)
    file_list = glob.glob(folder)
    return file_list
'''
def main():
    input_folder = sys.argv[1]
    model_name = sys.argv[2]
    feature_list = layer_feature_extraction(input_folder,
                                 model_name, layer_name='avg_pool')
    result = pd.DataFrame(feature_list)
    result = result.transpose()
    retuls.to_pickle(sys.argv[3])
'''
if __name__ == '__main__':
    main()
