#!/usr/bin/env python
# coding: utf-8

# # Pacotes e configurações

# In[1]:


import pandas as pd


# # Importação dos dados

# In[2]:


# Arquivo com as informações de ocorrência, tempo localidade, e outras variáveis de análise.
df = pd.read_csv('df_final_4.csv')

# Identificador e coluna de tempo
data  = pd.read_csv('dim_tempo_202305212244.csv')


# # Limpeza dos arquivos

# In[3]:


# Realizar o merge dos DataFrames com base nas colunas "id_tempo_x" e "id_tempo"
df = pd.merge(df, data[['id_tempo', 'tempo']], left_on='id_tempo_x', right_on='id_tempo', how='left')

# Preencher os valores nulos na coluna "tempo_x" com os valores correspondentes
df['tempo_x'].fillna(df['tempo_y'], inplace=True)

# Remover colunas desnecessárias após o preenchimento
df.drop(['id_tempo', 'tempo_y'], axis=1, inplace=True)

df.rename(columns={'tempo_x': 'tempo'}, inplace=True)


# # Avaliar a completude dos dados em cada estação ao longo do tempo

# In[4]:


df['yyyy-mm'] = pd.to_datetime(df['tempo']).dt.strftime('%Y-%m')

df_tempo = df[['id_estacao','yyyy-mm','tempo']].drop_duplicates()

df_dias = df_tempo.groupby(['id_estacao','yyyy-mm'])['tempo'].count().reset_index(name='Qtd_dias')

#df_dias
# lista = [501, 508, 515, 500, 516, 524, 528, 522, 517, 506, 503, 529]


# # Verificar as ocorrências por estação no tempo de estudo

# In[5]:


df_ocorr = df.groupby(['id_estacao', 'yyyy-mm']).agg({'ocorrencia': 'sum', 'vintequatrohoras': ['min', 'mean', 'max']}).reset_index()

# df.groupby(['id_estacao']).agg({'ocorrencia': 'sum', 'n_coord': 'nunique'}).reset_index()


# # Retirar estações ruins

# In[6]:


#estacoes_ruins = lista
#df = df[~df['id_estacao'].isin(estacoes_ruins)]


# # Salvar arquivos

# In[7]:


df.to_csv('df_limpo.csv')

df_dias.to_csv('df_teste.csv')

df_ocorr.to_csv('df_analise.csv')

