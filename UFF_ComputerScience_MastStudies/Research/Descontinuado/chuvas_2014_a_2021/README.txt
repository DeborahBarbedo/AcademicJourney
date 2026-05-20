## Detalhamento dos Dados Pluviométricos (Séries Temporais)

Os arquivos de dados pluviométricos contêm o histórico de chuvas do município, estruturados em séries temporais ordenadas de forma cronológica crescente. Cada arquivo armazena as medições consolidadas de **um ano específico**.

Esses dados fornecem o comportamento dinâmico do pipeline, atuando como o gatilho principal (*trigger*) para a modelagem preditiva de instabilidade de encostas.

### Dicionário de Variáveis

| Coluna | Tipo | Descrição |
| :--- | :--- | :--- |
| `tempo` | *Datetime* | Data e hora do registro da chuva, padronizado no formato `YYYY-mm-dd HH:MM:SS`. |
| `id_estacao` | *Integer* | Identificador exclusivo e unívoco da estação pluviométrica. |
| `nome_estacao_original` | *String* | Nome descritivo da estação. **Nota:** Há casos de estações com o mesmo nome, mas localizações e IDs diferentes (conforme mapeado em `estacoes_niteroi.csv`). Use sempre `id_estacao` como chave primária. |
| `indice_pluv` | *Float* | Índice pluviométrico medido especificamente no instante exato do registro. |

### Atributos de Acumulados Temporais (*Lag Features*)
As colunas abaixo representam o volume de chuva acumulado (em mm) em diferentes janelas de tempo retrospectivas até o instante do registro.

* **Janelas de Curto Prazo (Imediato):**
    * `quinzemin`: Acumulado nos últimos 15 minutos.
    * `trintamin`: Acumulado nos últimos 30 minutos.
    * `umahora`: Acumulado na última 1 hora.
* **Janelas de Médio Prazo (Saturação Superficial):**
    * `seishoras`: Acumulado nas últimas 6 horas.
    * `dozehoras`: Acumulado nas últimas 12 horas.
    * `vintequatrohoras`: Acumulado nas últimas 24 horas.
* **Janelas de Longo Prazo (Saturação Profunda / Crítica):**
    * `quarentaoitohoras`: Acumulado nas últimas 48 horas.
    * `setentaduashoras`: Acumulado nas últimas 72 horas.
    * `noventaseishoras`: Acumulado nas últimas 96 horas.
    * `mes`: Acumulado no último mês (30 dias).

---

### ⚠️ Notas de Pré-processamento Importantes para o Modelo:
1.  **Chave Composta:** Para qualquer agrupamento (`groupby`) ou pivotação de séries temporais, utilize sempre a combinação de `tempo` + `id_estacao` para evitar que dados de estações homônimas sejam somados incorretamente.
2.  **Dados Faltantes (Missing Values):** Como mencionado no pipeline, falhas de transmissão de telemetria nas estações podem gerar lacunas nessas janelas. O script `Limpeza_dados_Missing` trata essas ocorrências antes de enviar os dados para os modelos.