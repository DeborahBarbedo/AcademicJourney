# Especificação do Pipeline de Dados e Arquivos de Entrada

O fluxo segue uma ordem cronológica de execução, desde a amostragem espacial até a preparação final dos dados para os modelos.

---

## 1. Amostragem e Mapeamento Espacial (`Sample_coordenadas`)

Este script realiza a amostragem espacial do terreno. Ele atribui um identificador único de coordenada a pontos selecionados por meio do método **Poisson Disc Sampling**. Em seguida, associa as ocorrências históricas de deslizamentos à coordenada amostrada mais próxima dentro de um raio de 50 metros. Caso não exista uma ocorrência registrada nas proximidades, uma nova instância de "não-ocorrência" (classe negativa) é gerada para essa nova coordenada.

* **📥 Arquivos de Entrada:**
    * `ocorrencias.csv` (Histórico de eventos da Defesa Civil)
* **📤 Arquivos de Saída:**
    * `coordenadas_mapeadas.csv` (Dicionário de pontos amostrados)
    * `amostra_aleatoria_coord_100m.csv` (Malha de pontos de controle)

---

## 2. Enriquecimento e Engenharia de Atributos (`Atribuicao_variáveis`)

Este script é o núcleo da engenharia de atributos (*feature engineering*). Ele cruza os pontos espaciais gerados no passo anterior com múltiplas fontes de dados (rasters, vetores e séries temporais) para extrair as variáveis preditivas do modelo.

* **📥 Arquivos de Entrada:**
    * **Bases Espaciais:** `coordenadas_mapeadas.csv`, `amostra_aleatoria_coord_100m.csv`
    * **Variáveis Geomorfológicas (Raster):** Arquivos `.tif` (TOPODATA/INPE)
    * **Variáveis Ambientais (Vetores IBGE):** `vege_area_mu_3303302.zip`, `pedo_area_mu_3303302.zip`
    * **Variáveis Locais (Vetores SIGeo):** `Unidades_de_Conservacao_Integral.geojson`, `Comunidades.geojson`, `areas_de_risco_Defesa_Civil.geojson`
    * **Variáveis Climáticas / Proximidade:** `voronoi_prefeitura.csv`, `Tempo_estacao_24h.csv`
* **📤 Arquivos de Saída:**
    * `coordenadas_mapeadas_variaveis.csv`
    * `df_final_4.csv` (Dataset consolidado com todas as features)

---

## 3. Sanidade e Consistência de Dados (`Validacao_Medidores`)

Script responsável pelo controle de qualidade e auditoria. Ele verifica a integridade dos dados gerados no cruzamento anterior, garantindo a consistência temporal e espacial das medições antes do treinamento.

* **📥 Arquivos de Entrada:**
    * `df_final_4.csv` (Dataset consolidado)
    * `dim_tempo_202305212244.csv` (Tabela dimensão de tempo para validação)
* **📤 Arquivos de Saída:**
    * `df_analise.csv` (Dados formatados para análise exploratória básica)
    * `df_limpo.csv` (Base validada filtrada para os próximos passos)
    * `df_teste.csv` (Subset isolado para validação final dos modelos)

---

## 4. Pré-processamento: Escalonamento (`Limpeza_dados_Normalizacao`)

Garante que os dados numéricos estejam na mesma escala, evitando que variáveis com ordens de grandeza muito diferentes distorçam o treinamento dos modelos de Machine Learning e Deep Learning.

* **📥 Arquivos de Entrada:**
    * `df_limpo.csv`
* **📤 Arquivos de Saída:**
    * `df_norm.csv` (Dataset com variáveis numéricas normalizadas/padronizadas)

---

## 5. Pré-processamento: Tratamento de Missing Data (`Limpeza_dados_Missing`)

Fase final de tratamento de dados. Trata registros ausentes (*missing values*) gerados por falhas pontuais em estações meteorológicas ou lacunas de sensores, utilizando técnicas de imputação apropriadas para séries temporais.

* **📥 Arquivos de Entrada:**
    * `df_norm.csv`
* **📤 Arquivos de Saída:**
    * `df_comp2.csv` (**Dataset Final Pronto para Modelagem:** limpo, enriquecido, normalizado e sem dados faltantes).