#!/usr/bin/env python
# coding: utf-8

# # Pacotes

# In[ ]:


import pandas as pd
import numpy as np

from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns
from prettytable import PrettyTable
import sklearn
from sklearn.metrics import confusion_matrix

import time
from tensorflow import keras
import tensorflow as tf
from keras.models import Sequential
from keras.models import Sequential
from keras.layers import Dense, LSTM, Bidirectional, Flatten #Global max pullin avg max pulling
from keras.layers import  Masking
from keras.regularizers import l2, L1L2
from keras import regularizers 

from keras.callbacks import EarlyStopping, ModelCheckpoint

import datetime

tf.config.list_physical_devices('GPU')

# fix random seed for reproducibility
seed = 42
tf.random.set_seed(seed)


# # Funcoes

# In[ ]:


##############################
###### Matriz de confusão ####
##############################

def matriz_confusao(y_real,y_predito,modelo):

### Grafico ###

  tabela=confusion_matrix(y_real,y_predito)

  group_names = ["True Neg","False Pos","False Neg","True Pos"]
  group_counts = ["{0:0.0f}".format(value) for value in
                tabela.flatten()]
  group_percentages = ["{0:.5%}".format(value) for value in
                     tabela.flatten()/np.sum(tabela)]
  labels = [f"{v1}\n{v2}\n{v3}" for v1, v2, v3 in
          zip(group_names,group_counts,group_percentages)]
  labels = np.asarray(labels).reshape(2,2)
  f = plt.figure()
  f.set_figwidth(8)
  f.set_figheight(8)

  sns.heatmap(tabela, annot=labels, fmt="", cmap='Blues')

### Tabela ###
  Resultados=PrettyTable()
  Resultados.field_names=["Métrica","Resultado"]
  Resultados.title= modelo
  Resultados.align["Métrica"]="l"
  Resultados.align["Resultado"]="r"

  Resultados.add_row(["Acurácia:",round(sklearn.metrics.accuracy_score(y_real,y_predito),2)])
  Resultados.add_row(["Precisão:",round(sklearn.metrics.precision_score(y_real,y_predito),2)])
  Resultados.add_row(["Recall:",round(sklearn.metrics.recall_score(y_real,y_predito),2)])
  Resultados.add_row(["F1-Score:",round(sklearn.metrics.f1_score(y_real,y_predito),2)])

  print(Resultados)
  
  return



    
def transformacao_estrutura(df, lista_variaveis):
    '''
    Extrai os atributos do dataframe pandas

    Params:
    -------
    df: dataframe de entrada

    Returns:
    par X, Y
    '''

    X = df[lista_variaveis]
    


    
    Y = df[['ocorrencia']]
    
    n_tempo, n_coord = conta_tempos_e_coordenadas(df)
    
    X_transformado = X.to_numpy().astype(np.float32).reshape(n_tempo , n_coord, -1)
    Y_transformado = Y.to_numpy().astype(np.float32).reshape(n_tempo , n_coord, -1)
    
    return X_transformado, Y_transformado

    
def conta_tempos_e_coordenadas(df):
    '''
    Conta o número de tempos e coordenadas de um dataframe

    Params:
    -------
    df: dataframe com os atributos 'tempo', e 'n_coord'

    Returns:
    --------
    tupla número de tempos, número de coordenadas
    '''
    tempo = len(df['tempo'].unique())
    n_coord = len(df['n_coord'].unique())

    return tempo, n_coord


def calcula_sample_weight(df,peso):
    '''
    Calcula os pesos para as amostras de treinamento
    '''
    
    Y = df[['ocorrencia']]
    sample_weight_ = list(Y['ocorrencia'])
    
    series = pd.Series(sample_weight_)
    series = series*peso #3191848/613
    series = series+1
    series = series/(peso+1)
    
    sample_weight_ = np.array(list(series)).astype(np.float32)
    
    return sample_weight_
    
    
def flatten(l):
    return [item for sublist in l for item in sublist]    


# # Importacao dos dados

# In[ ]:


df = pd.read_csv('df_comp.csv')


# In[ ]:


df.replace(np.nan,-1, inplace=True)


# In[ ]:


df['tempo'] =  pd.to_datetime(df['tempo'])


# In[ ]:


df = df.sort_values(['tempo','n_coord'])


# In[ ]:


lista_variaveis = [
     'vintequatrohoras'                                
    ,'Altitude_numerica'                               
    ,'Declividade_numerica'                          
    ,'graurisc'                                        
    ,'lon_ocr'                                         
    ,'lat_ocr'                                         
    ,'Orientacao_numerica'                             
    ,'Curv_Vertical_numerica'                          
    ,'Curv_Horizontal_numerica'                        
    ,'Relevo_sombreado_numerico'                       
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
    ,'flg_favela'                                      
    ,'flg_ocupacao_desordenada'                         
           ]


# Manter fixo:
# 
# * Teste  - 3 meses
# 
# Deslizar:
# 
# * Treinamento - 2 anos
# 
# * Validação - 6 meses

# In[ ]:


janela_treino = ['2019-02-24 09:00:00'
                ,'2019-03-24 09:00:00'
                ,'2019-04-24 09:00:00'
                ,'2019-05-24 09:00:00'
                ,'2019-06-24 09:00:00'
                ,'2019-07-24 09:00:00'
                ,'2019-08-24 09:00:00'
                ,'2019-09-24 09:00:00'
                ,'2019-10-24 09:00:00'
                ,'2019-11-24 09:00:00'
                ,'2019-12-24 09:00:00'
                ,'2020-01-24 09:00:00'
                ,'2020-02-24 09:00:00'
                ,'2020-03-24 09:00:00'
                ,'2020-04-24 09:00:00'
                ,'2020-05-24 09:00:00'
                ]

janela_validacao_i = ['2021-02-24 09:00:00'
                ,'2021-03-24 09:00:00'
                ,'2021-04-24 09:00:00'
                ,'2021-05-24 09:00:00'
                ,'2021-06-24 09:00:00'
                ,'2021-07-24 09:00:00'
                ,'2021-08-24 09:00:00'
                ,'2021-09-24 09:00:00'
                ,'2021-10-24 09:00:00'
                ,'2021-11-24 09:00:00'
                ,'2021-12-24 09:00:00'
                ,'2022-01-24 09:00:00'
                ,'2022-02-24 09:00:00'
                ,'2022-03-24 09:00:00'
                ,'2022-04-24 09:00:00'
                ,'2022-05-24 09:00:00'
                ]

janela_validacao_s = ['2021-08-24 09:00:00'
                ,'2021-09-24 09:00:00'
                ,'2021-10-24 09:00:00'
                ,'2021-11-24 09:00:00'
                ,'2021-12-24 09:00:00'
                ,'2022-01-24 09:00:00'
                ,'2022-02-24 09:00:00'
                ,'2022-03-24 09:00:00'
                ,'2022-04-24 09:00:00'
                ,'2022-05-24 09:00:00'
                ,'2022-06-24 09:00:00'
                ,'2022-07-24 09:00:00'
                ,'2022-08-24 09:00:00'
                ,'2022-09-24 09:00:00'
                ,'2022-10-24 09:00:00'
                ,'2022-11-24 09:00:00'
                ]


# In[ ]:


df_saida_modelo = pd.DataFrame({'Janela': None
                    ,'Treino Ocorrências': None
                    ,'#Treino': None
                    ,'Validação Ocorrências': None
                    ,'#Validação': None
                    ,'Teste Ocorrências': None
                    ,'#Teste': None
                    
                    ,'loss': None
                    ,'binary_crossentropy': None
                    ,'accuracy': None
                    ,'precision': None
                    ,'recall': None
                                
                    ,'Verdadeiro Negativo': None
                    ,'Falso Positivo': None
                    ,'Falso Negativo': None
                    ,'Verdadeiro Positivo': None            
                                 }, index=[0])


# In[ ]:


for i in range(len(janela_validacao_s)):
    print('#'*20)
    print('#'*20)
    print('Modelo 5')
    print(f' Janela {i}')
    print('#'*20)
    print('#'*20)
    
    saida_modelo = [i+1]
    
    filtro_inferior = pd.to_datetime(janela_treino[i]) <= df.loc[:, 'tempo']
    filtro_superior = df.loc[:,'tempo'] < pd.to_datetime(janela_validacao_i[i])
    treino = df[filtro_inferior & filtro_superior]
    
    filtro_inferior = pd.to_datetime(janela_validacao_i[i]) <= df.loc[:, 'tempo']
    filtro_superior = df.loc[:, 'tempo'] < pd.to_datetime(janela_validacao_s[i])
    validacao = df[filtro_inferior & filtro_superior]
    
    teste = df[df.loc[:,'tempo'] > pd.to_datetime('2022-11-24 09:00:00')]
    
    ### Treino

    X_train, Y_train = transformacao_estrutura(treino, lista_variaveis)

    ### Validação

    X_val, Y_val = transformacao_estrutura(validacao, lista_variaveis)

    ### Teste

    X_teste, Y_teste = transformacao_estrutura(teste, lista_variaveis)
    
    
    print('Treino Ocorrências, #Treino, Validação Ocorrências, #Validação, Teste Ocorrências, #Teste')
    T_qtd_o = sum(treino['ocorrencia'])
    T_tam_o = len(treino['ocorrencia'])
    peso = T_tam_o / T_qtd_o


    V_qtd_o = sum(validacao['ocorrencia'])
    V_tam_o = len(validacao['ocorrencia'])

    Tes_qtd_o = sum(teste['ocorrencia'])
    Tes_tam_o = len(teste['ocorrencia'])

    print(f'{T_qtd_o},{T_tam_o},{V_qtd_o},{V_tam_o},{Tes_qtd_o},{Tes_tam_o}')
    
    saida_modelo.extend([T_qtd_o,T_tam_o,V_qtd_o,V_tam_o,Tes_qtd_o,Tes_tam_o])
    
    sample_weight_ = np.asarray(calcula_sample_weight(treino,round(peso))).astype(np.float32)
    
    sample_weight_transformado = sample_weight_.reshape(len(treino['tempo'].unique()), len(treino['n_coord'].unique()), -1)
    
    
    ##################### Modelo ##################
    
    time_step = X_train.shape[1] # Quantidade de coordenada para equivaler a 1 espaço de tempo
    input_dim = X_train.shape[2] #qtd colunas (features)
    out = Y_train.shape[2]

    # LSTM
    start = time.time()
    model = Sequential()
    model.add(Masking(mask_value=-1.,input_shape=(time_step, input_dim,))) #camada de entrada
    model.add(LSTM(32,activation='elu', input_shape=(time_step, input_dim,),return_sequences=True, go_backwards=True
                  , kernel_regularizer= regularizers.L1L2(l1=0.01, l2=0.01))) # camada escondida
    model.add(Dense(out, activation='sigmoid')) #camada saida

    opt = tf.keras.optimizers.Adam(learning_rate=0.01)

    model.compile(loss = tf.keras.losses.BinaryCrossentropy(from_logits=False) #https://keras.io/api/losses/probabilistic_losses/ 
                  , optimizer= opt #'adam'
                  , weighted_metrics=[tf.keras.losses.BinaryCrossentropy(from_logits=False),'accuracy'
                  , tf.keras.metrics.Precision()
                  , tf.keras.metrics.Recall()]
                 , sample_weight_mode="temporal"   #Weights
                 )   
    model.summary()
    hist = model.fit(X_train
                     , Y_train
                     , epochs=100
                     ,validation_data=(X_val, Y_val)
                     , verbose=1
                     , batch_size=64
                     , sample_weight=sample_weight_transformado  #(samples, sequence_length)
            )
    end = time.time()
    print("Total compile time: --------", end - start, 's')
    
    predictions = (model.predict(X_teste, verbose=1) > 0.5).astype("int32").reshape((1,-1))
    
    score = model.evaluate(X_teste, Y_teste)
    
    print('loss, binary_crossentropy, accuracy, precision, recall ')
    print(f'{score}')
    
    saida_modelo.extend(score)
    
    pred_y = pd.DataFrame(flatten(predictions), columns=['Prediction']) 
    
    
    tabela=confusion_matrix(teste[['ocorrencia']],pred_y)
        
    print('Verdadeiro Negativo, Falso Positivo, Falso Negativo, Verdadeiro Positivo')
    print(f'{tabela[0,0]},{tabela[0,1]},{tabela[1,0]},{tabela[1,1]}')

    saida_modelo.extend(tabela.flatten())
    
    
    df_saida_modelo.loc[i] = saida_modelo


# In[ ]:


df_saida_modelo.to_csv('Modelo5E1.csv')

