#!/usr/bin/env python
# coding: utf-8

# <h1>Table of Contents<span class="tocSkip"></span></h1>
# <div class="toc"><ul class="toc-item"><li><span><a href="#Dataset-loader" data-toc-modified-id="Dataset-loader-1"><span class="toc-item-num">1&nbsp;&nbsp;</span>Dataset loader</a></span></li><li><span><a href="#Teste" data-toc-modified-id="Teste-2"><span class="toc-item-num">2&nbsp;&nbsp;</span>Teste</a></span><ul class="toc-item"><li><span><a href="#Print-datasets-info" data-toc-modified-id="Print-datasets-info-2.1"><span class="toc-item-num">2.1&nbsp;&nbsp;</span>Print datasets info</a></span></li><li><span><a href="#Get-dataset-list" data-toc-modified-id="Get-dataset-list-2.2"><span class="toc-item-num">2.2&nbsp;&nbsp;</span>Get dataset list</a></span></li><li><span><a href="#Load-data" data-toc-modified-id="Load-data-2.3"><span class="toc-item-num">2.3&nbsp;&nbsp;</span>Load data</a></span></li></ul></li></ul></div>

# ### Dataset loader
# 

# In[1]:


import numpy as np
import pandas as pd

import os
import json

import functools 


# Dataset loader para as bases NAB

# In[31]:


class DatasetLoader(object):
    
    def __init__(self, path='./data/', labels_path='./labels/combined_windows.json'):
        ''' path: deve os folders de cada dataset
            labels_path: path que contem o arquivo de labels combined_windows.json
        '''
        self.path = path
        self.datasets = self.__datasets_name(path)
        self.labels = self.__get_labels(labels_path)
    
    def print_all(self):
        ''' print the dataset list '''
        for k, datasets in self.datasets.items(): 
            print(k + ':')
            for ds in datasets:
                print(' '*5 + ds)
                
    def get_list(self, category=None):
        # datasets de uma categoria
        if category is not None:
            return self.datasets[category]
        # todos os datasets
        return functools.reduce(lambda x, y: x + y, 
                                list(self.datasets.values()))
    
    def load(self, name):
        '''
            returns: Tuple(data, labels)
            data, labels: dataframe 
        '''
        for n in self.datasets.keys():
            if name in self.datasets[n]:
                # data
                df = pd.read_csv(self.path + n + '/' + name)
                df['timestamp'] = pd.to_datetime(df['timestamp'], format='%Y/%m/%d %H:%M:%S')
                df.set_index('timestamp', inplace=True)
                # label
                label = self.__labels(n + '/' + name)
                
                return df, label
        
    def __datasets_name(self, path):
        datasets = {}
        folders = os.listdir(path)
        for f in folders: datasets[f] = os.listdir(path + f)
        return datasets
    
    def __get_labels(self, path):
        with open(path) as f:
            labels = json.load(f)

        return labels
    
    def __labels(self, name):
        if self.labels[name] == []:
            return None
        
        true_windows = pd.DataFrame(self.labels[name])
        true_windows[0] = pd.to_datetime(true_windows[0], format='%Y/%m/%d %H:%M:%S')
        true_windows[1] = pd.to_datetime(true_windows[1], format='%Y/%m/%d %H:%M:%S')
        true_windows.columns=['start', 'end']
        return true_windows


# ### Teste

# #### Print datasets info

# In[32]:


#loader = DatasetLoader()
#loader.print_all()


# #### Get dataset list

# In[33]:


#ds_list = loader.get_list()
#ds_list[:10]


# In[34]:


#loader.get_list('realTweets')


# #### Load data

# In[35]:


#for ds in ds_list:
#    df = loader.load(ds)
#    
#    if df is not None:
#        print(ds + ': ok')
#    else:
#        print(ds + ': ERROR')


# In[37]:


#df, label = loader.load(ds_list[0])
#df.plot()


# In[38]:


#df, label = loader.load(ds_list[20])
#df.plot()


# In[39]:


#df, label = loader.load('nyc_taxi.csv')
#df.plot()

