#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
from numpy.random import seed 

import sklearn
from sklearn.neighbors import KNeighborsClassifier

from sklearn.metrics import auc
from sklearn.metrics import roc_curve
seed(1)
from sklearn.model_selection import StratifiedKFold
import matplotlib
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score,f1_score, precision_score, recall_score
from imblearn.over_sampling import SMOTE
from sklearn.preprocessing import StandardScaler, MinMaxScaler

from joblib import dump

# In[2]:


df_gaff = pd.read_csv('gaff.txt', header = None, sep = '\t')
df_rdkit = pd.read_csv('rdkit.txt', header = None, sep = '\s+')


# In[3]:


df_gaff = df_gaff.set_index(0)
df_rdkit = df_rdkit.set_index(0)


# In[4]:


df_rdkit_noyw =df_rdkit.drop(columns=[1,2])


# In[5]:


df_rdkit_noyw.columns = range(50,258)


# In[6]:


df = pd.concat([df_gaff,df_rdkit_noyw], axis=1)


# In[7]:


df=df.dropna(axis=0)


# In[11]:


X = df.drop(columns = [1,2])
y = df[1]


# In[12]:


scaler = MinMaxScaler()
scaler.fit(X)
X = scaler.transform(X)


# In[14]:


sm = SMOTE(random_state=1)
X_res, y_res = sm.fit_resample(X,y)


# ## Training

# In[16]:

clf = KNeighborsClassifier(n_neighbors=7)

clf.fit(X_res, y_res)

dump(clf,'/home2/bej22/projects/covid19/ncats_modeling/rdkit_gaff/assay6/assay6.joblib')
