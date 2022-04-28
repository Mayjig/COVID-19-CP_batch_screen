#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
import sklearn
from sklearn.preprocessing import MinMaxScaler
import joblib


# In[2]:


PATH = '/home2/bej22/projects/covid19/ncats_modeling/rdkit_gaff'

TRAIN_RDKIT_FILE = 'rdkit.txt'
TRAIN_GAFF_FILE = 'gaff.txt'

TEST_RDKIT_FILE = 'rdkit_test.txt'
TEST_GAFF_FILE = 'gaff_test.txt'

MODEL_NAME_LIST = ['assay']
OUPUT_FILE = 'classification_result.csv'


# In[3]:


# ===================================
# ==== Train Data Transformation ====
# ===================================
def process_train_data(rdkit, gaff):
    df_rdkit = pd.read_csv(rdkit, header = None, sep = '\s+')
    df_gaff = pd.read_csv(gaff, header = None, sep = '\t')
    df_rdkit = df_rdkit.set_index(0)
    df_gaff = df_gaff.set_index(0)
    df_rdkit_noyw =df_rdkit.drop(columns=[1,2])
    df_rdkit_noyw.columns = range(50,258)
    df = pd.concat([df_gaff,df_rdkit_noyw], axis=1)
    df=df.dropna(axis=0)

    return df


# In[4]:


# ====================================
# ===== Test Data Transformation =====
# ====================================
def process_test_data(rdkit, gaff):
    df_test_rdkit = pd.read_csv(rdkit, header = None, sep = '\s+')
    df_test_gaff = pd.read_csv(gaff, header = None, sep = '\t')
    df_test_rdkit = df_test_rdkit.set_index(df_test_gaff[0])
    #df_test_rdkit = df_test_rdkit.set_index(0)
    df_test_gaff = df_test_gaff.set_index(0)
    df_test_rdkit.columns = range(48,256)
    df_test = pd.concat([df_test_gaff,df_test_rdkit], axis=1)
    df_test=df_test.dropna(axis=0)

    return df_test


# In[5]:


def load_model(name, n):
    file_path = PATH + '/assay' + n + '/' + name + n + '.joblib'
    return joblib.load(file_path)


# In[6]:


if __name__ == '__main__':
    df = process_train_data(PATH + '/' + TRAIN_RDKIT_FILE, PATH + '/' + TRAIN_GAFF_FILE)
    df_test = process_test_data(PATH + '/' + TEST_RDKIT_FILE, PATH + '/' + TEST_GAFF_FILE)

    train_X = df.drop(columns = [1,2])

    test_X = df_test
    scaler = MinMaxScaler()
    scaler.fit(train_X)
    test_X = scaler.transform(test_X)
    
    index = [
        '3CL enzymatic activity',
        'ACE2 enzymatic activity',
        'TMPRSS2 enzymatic activity',
        'Spike-ACE2 protein-protein interaction AlphaLISA',
        'Spike-ACE2 protein-protein interaction TruHit Counterscreen',
        'HEK293 cell line toxicity',
        'Human fibroblast toxicity',
        'SARS-CoV-2 cytopathic effect CPE',
        'SARS-CoV-2 cytopathic effect host tox counterscreen'
        ]

    value = []
    result = []
    active = [1, 1, 1, 1, 0, 0, 0, 1, 0]
    viewData = []


# In[7]:


value=[]
viewData=[]
for n in range(1, 10):
        preds = []
        data = []
        count = 0

        for i in range(0,len(test_X)):
            model = load_model(MODEL_NAME_LIST[0], str(n))

            pred_prob = model.predict_proba(test_X)[:,1][i]
            pred = model.predict(test_X)[i]
            preds.append(pred)
            #preds.append(pred_prob.round(2))
            #data.append(pred)

        value.append(preds)
        #viewData.append(data)


# In[21]:


estimation = pd.DataFrame(np.array(value), columns = df_test.index , index = index)
#viewDataDf = pd.DataFrame(np.array(viewData))
estimation.index.name='Assay'
estimation.to_csv(PATH + '/' + OUPUT_FILE, index = True, header = True)
#viewDataDf.to_csv(PATH + '/' + 'view.csv', index = False, header = False)
# joblib_svm_file = "joblib_svm.pkl"  
compound = pd.DataFrame(df_test.reset_index()[0])
compound.to_csv(PATH + '/' + 'compname.csv', index=False, header=False)


# In[ ]:




