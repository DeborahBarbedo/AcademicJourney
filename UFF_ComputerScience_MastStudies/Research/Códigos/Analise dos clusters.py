#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
#df = pd.read_csv('coordenadas_mapeadas_variaveis.csv')


# In[2]:


clusters = pd.read_csv('coord_cluster.csv')


# In[3]:


clusters


# In[4]:


df_C = pd.merge(df, clusters, how='inner', left_on=['n_coord'], right_on=['n_coord'])


# In[5]:


df_C


# In[9]:


from matplotlib import pyplot as plt


# In[10]:


import seaborn as sns


# In[12]:


plt.figure(figsize= (20,10))
sns.histplot(data = df_C, x = 'Cluster', hue = 'flg_cobertura_vegetal' ,  stat="percent", discrete=True )


# In[13]:


df_C['flg_cobertura_vegetal'].value_counts()


# In[14]:


plt.figure(figsize= (20,10))
sns.histplot(data = df_C, x = 'Cluster', hue = 'Altitude_numerica' ,  stat="percent", discrete=False )


# In[5]:


df = pd.read_csv('df_comp2.csv')

#Separacao Cluster

clusters = pd.read_csv('coord_cluster_6.csv')

df_aux = pd.merge(df, clusters, how='inner', left_on=['n_coord'], right_on=['n_coord'])

df = df_aux[df_aux['Cluster']==1]


# In[6]:


df


# In[ ]:




