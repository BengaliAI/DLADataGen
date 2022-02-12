# -*-coding: utf-8 -
'''
    @author: MD. Nazmuddoha Ansary
'''
#--------------------
# imports
#--------------------
import os
import pandas as pd 
from glob import glob
from tqdm.auto import tqdm
from .utils import *
tqdm.pandas()
#--------------------
# class info
#--------------------

        
class DataSet(object):
    def __init__(self,data_dir):
        '''
            Instance creation for data sources:
            -> font
                -> language 
            -> signs
            -> logo
        '''
        self.data_dir=data_dir
        self.font_dir=os.path.join(self.data_dir,"fonts")
        
        class fonts:
            bangla = [font_path for font_path in tqdm(glob(os.path.join(self.font_dir,"bangla","*.ttf")))]
            LOG_INFO(f"Collected bangla font paths:{len(bangla)}")
            english = [font_path for font_path in tqdm(glob(os.path.join(self.font_dir,"english","*.ttf")))]
            LOG_INFO(f"Collected english font paths:{len(english)}")
        # font
        self.fonts=fonts

        # sign
        self.signs=[sign_img_path for sign_img_path in tqdm(glob(os.path.join(self.data_dir,"signs","*.*")))]
        LOG_INFO(f"Collected sign paths:{len(self.signs)}")
        
 
 