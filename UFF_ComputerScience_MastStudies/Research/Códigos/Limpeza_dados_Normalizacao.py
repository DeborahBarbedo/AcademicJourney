#!/usr/bin/env python
# coding: utf-8

# # Pacotes

# In[1]:


import pandas as pd
import numpy as np


# # Funcoes

# Funcoes originarias de : 
# 
#     Model for SPATIAL and data cleaning
#     
#     https://github.com/IBM/spatial-lstm/blob/a18fb9fda2d9c8e5311cf1f46e3173f82a21ad24/Model/model.py#L163

# In[2]:


########################
###### Normalizador ####
########################


def normalizador_min_max(dados, variaveis):
    
    for j in variaveis:
        menor = min(dados[str(j)]) 
        maior = max(dados[str(j)])
        
        dif = maior - menor
        if dif==0:
            dif=1 
        
        for i in range(dados.shape[0]):
            dados.loc[i,j] = (dados[str(j)][i]-menor)/ dif

    return(dados) 


def normalizador_log(dados, variaveis):
    for j in variaveis:
        for i in range(dados.shape[0]):
            if pd.notnull(dados.loc[i, str(j)]) and dados.loc[i, str(j)] > 0:
                dados.loc[i, str(j)] = np.log(dados.loc[i, str(j)])
            else:
                dados.loc[i, str(j)] = np.log(1e-5)

    return dados 


# # Importacao dos dados

# In[5]:


df = pd.read_csv('df_limpo.csv').drop(columns=['Unnamed: 0'])


# In[6]:


df


# Transformação logarítimica para variáveis com distribuição assimétrica e variáveis com muitos zeros.

# In[7]:


normalizador_log(df, ["vintequatrohoras", "Altitude_numerica", "Declividade_numerica", "graurisc"])


# Transformação min-max para variáveis com distribuições semelhantes da normal.

# In[8]:


normalizador_min_max(df, ['lon_ocr', 'lat_ocr', 'Orientacao_numerica', 'Curv_Vertical_numerica', 'Curv_Horizontal_numerica', 'Relevo_sombreado_numerico'])


# In[9]:


#df.hist(bins=30, figsize=(30,30))


# In[10]:


#df = df.interpolate(method ='linear')


# In[11]:


df.to_csv('df_norm.csv')


# In[12]:


df


# In[ ]:




