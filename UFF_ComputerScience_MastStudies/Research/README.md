# Previsão de Deslizamentos de Terra em Niterói

![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)
![Data Science](https://img.shields.io/badge/Data%20Science-Project-green.svg)
![Machine Learning](https://img.shields.io/badge/Machine%20Learning-Deep%20Learning-orange.svg)

Este repositório reúne os arquivos, códigos, dados e documentos utilizados no desenvolvimento de modelos de previsão de deslizamentos de terra no município de Niterói, como parte do projeto **PDPA** (Programa de Desenvolvimento de Projetos Aplicados) da Prefeitura de Niterói.

O objetivo principal é apoiar ações de monitoramento, prevenção e mitigação de riscos geotécnicos por meio de técnicas de **Ciência de Dados**, **Machine Learning** e análise de séries temporais, integrando informações meteorológicas, geográficas e geotécnicas.

---

## 🎯 Objetivos do Projeto

*   Desenvolver modelos preditivos acurados para o risco de deslizamentos de terra.
*   Apoiar sistemas locais de alerta precoce e defesa civil.
*   Integrar dados complexos espaciais, temporais e ambientais.
*   Avaliar e aplicar técnicas robustas para o tratamento de **dados altamente desbalanceados**.
*   Comparar o desempenho de diferentes arquiteturas tradicionais de Machine Learning e Deep Learning.

---

## 📁 Estrutura do Repositório

O projeto está organizado na seguinte estrutura de diretórios:

| Pasta | Descrição |
| :--- | :--- |
| `📂 Codigos` | Scripts e Jupyter Notebooks de pré-processamento, engenharia de atributos, treinamento e testes com Deep Learning (LSTM, CNN-LSTM). |
| `📂 Dados` | Conjuntos de dados brutos e processados provenientes de satélites, estações meteorológicas, sensores e modelos digitais de elevação. |
| `📂 Documentacao` | Materiais de apoio, artigos, relatórios técnicos, planilhas de evolução e avaliação de desempenho dos experimentos. |
| `📂 Descontinuado` | Arquivos, modelos e experimentos antigos mantidos exclusivamente para fins de rastreabilidade e histórico do projeto. |

---

## 🛠️ Tecnologias e Abordagens Utilizadas

O desenvolvimento deste projeto envolve o estado da arte em modelagem preditiva para desastres naturais:

*   **Modelagem Temporal e Espacial:** Redes neurais Recorrentes (**LSTM**), arquiteturas híbridas (**CNN-LSTM**) e classificação de séries temporais.
*   **Tratamento de Dados Desbalanceados:** Técnicas de *oversampling*, funções de perda customizadas (como *Focal Loss*) e métricas de avaliação apropriadas (Precision-Recall, F1-Score, AUC-PR).
*   **Análise de Domínio:** Processamento de dados pluviométricos (acumulados de chuva) e análise de variáveis geotécnicas.

---

## 🚀 Como Começar (Exemplo)

Se você deseja replicar os experimentos ou analisar os notebooks, siga os passos abaixo:

### 1. Clonar o Repositório
```bash
git clone [https://github.com/seu-usuario/seu-repositorio.git](https://github.com/seu-usuario/seu-repositorio.git)
cd seu-repositorio
