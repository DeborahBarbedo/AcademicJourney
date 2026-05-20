#!/usr/bin/env python
# coding: utf-8

# # Pacotes

# In[ ]:


import pandas as pd
import numpy as np


# # Importacao dos dados

# In[ ]:


df = pd.read_csv('df_norm.csv',index_col="tempo_x", parse_dates=True)

df = df.rename_axis('tempo')


# In[ ]:


df = df[['n_coord'
         ,'ocorrencia'
         , "vintequatrohoras"
         , "Altitude_numerica"
         , "Declividade_numerica"
         , "graurisc"
         , 'lon_ocr'
         , 'lat_ocr'
         , 'Orientacao_numerica'
         , 'Curv_Vertical_numerica'
         , 'Curv_Horizontal_numerica'
         , 'Relevo_sombreado_numerico'
         ,'Vegetacao_Natural_Dominante'                
,'Area_Antropica_Dominante'                   
,'legenda_2_Pecuária (pastagens)'             
,'Floresta_Ombrofila_Densa'                   
,'Formacao_Pioneira'                          
,'Floresta_Ombrofila_Densa_Submontana'        
,'Influencia_urbana'                          
,'Vegetacao_Secundaria'                       
,'Argilossolo'                                
,'Gleissolo'                                  
,'Argilossolo_Vermelho_Amarelo'               
,'Gleissolo_Melanico'                         
,'Area_Urbana'                                
,'Unidades_de_Conservacao_Protecao_Integral'  
,'Plano_de_Manejo'                            
,'flg_comunidades'                          
,'flg_agricola'                               
,'flg_exploracao_mineral'                     
,'flg_rocha'                                  
,'flg_cobertura_vegetal'                      
,'flg_afloramento_rochoso'                                                    
,'flg_ocupacao_desordenada' ]].sort_index()


# In[ ]:


print(df.index.min())
print(df.index.max())


# In[ ]:


df_coords = df[['n_coord'
         , "Altitude_numerica"
         , "Declividade_numerica"
         , "graurisc"
         , 'lon_ocr'
         , 'lat_ocr'
         , 'Orientacao_numerica'
         , 'Curv_Vertical_numerica'
         , 'Curv_Horizontal_numerica'
         , 'Relevo_sombreado_numerico'
         ,'Vegetacao_Natural_Dominante'                
,'Area_Antropica_Dominante'                   
,'legenda_2_Pecuária (pastagens)'             
,'Floresta_Ombrofila_Densa'                   
,'Formacao_Pioneira'                          
,'Floresta_Ombrofila_Densa_Submontana'        
,'Influencia_urbana'                          
,'Vegetacao_Secundaria'                       
,'Argilossolo'                                
,'Gleissolo'                                  
,'Argilossolo_Vermelho_Amarelo'               
,'Gleissolo_Melanico'                         
,'Area_Urbana'                                
,'Unidades_de_Conservacao_Protecao_Integral'  
,'Plano_de_Manejo'                            
,'flg_comunidades'                          
,'flg_agricola'                               
,'flg_exploracao_mineral'                     
,'flg_rocha'                                  
,'flg_cobertura_vegetal'                      
,'flg_afloramento_rochoso'                                                    
,'flg_ocupacao_desordenada' ]].drop_duplicates().reset_index(drop=True)


# In[ ]:


# Coordenadas
c = sorted(df_coords['n_coord'].unique())


# In[ ]:


coluna1 = [0]* len(df_coords['n_coord'].unique())
coluna2 = [np.nan]* len(df_coords['n_coord'].unique())

df_coords.insert(1, "ocorrencia", coluna1)
df_coords.insert(2, "vintequatrohoras", coluna2)


# In[ ]:


# Data 1 dia
df['tempo'] = df.index
d = sorted(df['tempo'].unique())


# In[ ]:


for i in d:
    
    sub_d = df[df.loc[:,'tempo'] == i]
    
    for j in c:
        
        if j not in sub_d[['n_coord']].values:
            
            aux = df_coords[df_coords.loc[:,'n_coord'] == j]
            aux = aux.assign(tempo=i)
            
            
            
            df = pd.concat([df, aux], ignore_index=True)


# In[ ]:


df['vintequatrohoras'] = df.groupby(['lat_ocr', 'lon_ocr']).apply(lambda x: x[['vintequatrohoras']].interpolate())


# In[ ]:


df.replace(np.nan,-1, inplace=True)


# In[ ]:


df.to_csv('df_comp2.csv')

