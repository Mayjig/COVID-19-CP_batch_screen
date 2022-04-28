#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
from numpy.random import seed 

import sklearn
from sklearn.neighbors import KNeighborsClassifier

seed(42)
from sklearn.metrics import auc
from sklearn.metrics import roc_curve

from sklearn.model_selection import StratifiedKFold
import matplotlib
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score,f1_score, precision_score, recall_score
from imblearn.over_sampling import SMOTE,RandomOverSampler
from sklearn.preprocessing import StandardScaler, MinMaxScaler

from joblib import dump

# In[2]:


dfc0_gaff = pd.read_csv('c0_gaff.txt', header = None, sep = '\t')
dfc1_gaff = pd.read_csv('c1_gaff.txt', header = None, sep = '\t')
dfc0_rdkit = pd.read_csv('c0_rdkit.txt', header = None, sep = '\s+')
dfc1_rdkit = pd.read_csv('c1_rdkit.txt', header = None, sep = '\s+')


# In[3]:


dfc0_gaff = dfc0_gaff.set_index(0)
dfc1_gaff = dfc1_gaff.set_index(0)
dfc0_rdkit = dfc0_rdkit.set_index(0)
dfc1_rdkit = dfc1_rdkit.set_index(0)


# In[4]:


df_gaff =  pd.concat([dfc0_gaff,dfc1_gaff])
df_rdkit =  pd.concat([dfc0_rdkit,dfc1_rdkit])


# In[5]:


df_rdkit_noyw =df_rdkit.drop(columns=[1,2])


# In[6]:


df_rdkit_noyw.columns = range(50,258)


# In[7]:


df = pd.concat([df_gaff,df_rdkit_noyw], axis=1)


# In[8]:


df=df.dropna(axis=0)

X = df.drop(columns = [1,2])
y = df[1]


# In[13]:


scaler = MinMaxScaler()
scaler.fit(X)
X = scaler.transform(X)


# In[15]:


#sm = SMOTE(random_state=1)
ros=RandomOverSampler(random_state=1)
X_res, y_res = ros.fit_resample(X,y)


# In[16]:

clf = KNeighborsClassifier(n_neighbors=5)

        
clf.fit(X_res, y_res)
       
dump(clf,'/home2/bej22/projects/covid19/ncats_modeling/assay1/rdkit_gaff/assay1.joblib') 
