### Dados Geomorfológicos (TOPODATA - INPE)

> ⚠️ **Nota de Armazenamento:** Devido ao grande volume e tamanho dos arquivos raster (`.tif`), os dados brutos do TOPODATA não estão versionados neste repositório (incluídos no `.gitignore`). Eles devem ser baixados diretamente do banco de dados do INPE e armazenados localmente na pasta `Dados/TOPODATA/`.

O projeto utiliza os dados da folha **22S435** (cobertura da região de Niterói/RJ), derivados do Modelo Digital de Elevação (MDE) do SRTM, processados pelo INPE. Cada sufixo de arquivo `.tif` corresponde a uma variável geomorfológica específica utilizada como atributo (*feature*) nos modelos:

| Nome do Arquivo | Variável Geomorfológica | Descrição / Uso no Modelo |
| :--- | :--- | :--- |
| `22S435ZN.tif` | **Altitude (Z)** | Altitude corrigida local (morfometria básica). |
| `22S435DD.tif` | **Declividade** | Inclinação do terreno (fator crítico para deslizamentos). |
| `22S435OC.tif` | **Orientação das Vertentes (Aspect)** | Direção para onde a encosta está virada (exposição solar/ventos). |
| `22S435V3.tif` | **Curvatura Vertical** | Caracteriza o perfil da encosta (convexa/côncava), afetando o fluxo de água. |
| `22S435V5.tif` | **Curvatura Horizontal** | Caracteriza a forma em plano da encosta, indicando divergência ou convergência de fluxos. |
| `22S435HN.tif` | **Sombreamento Relevo (Hillshade)** | Usado para visualização e relevo sombreado. |
| `22S435RS.tif` | **Radiação Solar** | Estimativa de radiação recebida na vertente. |
| `22S435ON.tif` | **Orientação Topográfica** | Variante de orientação para análise de fluxo e drenagem. |
| `22S435FT.tif` | **Formas de Terreno** | Classificação geomorfológica das feições locais. |
| `22S435H3.tif` / `H5.tif` | **Variáveis Hidrológicas** | Direção e acúmulo de fluxo/drenagem superficial. |
| `22S435SA.tif` a `SC.tif` | **Atributos de Curvatura Complementares** | Análises secundárias de aceleração e desaceleração de fluxo de água no solo. |

#### Como obter estes dados?
Os dados originais estão disponíveis gratuitamente no site oficial do projeto TOPODATA (INPE):
 [http://www.dsr.inpe.br/topodata/acesso.php](http://www.dsr.inpe.br/topodata/acesso.php)

### Dados Vetoriais Ambientais (IBGE)

Os vetores ambientais fornecidos pelo IBGE estão inclusos diretamente neste repositório na pasta `Dados/IBGE/`. Para manter a organização do diretório, os arquivos originais do formato Shapefile foram compactados em arquivos `.zip`:

* `pedo_area_mu_3303302.zip` — **Pedologia:** Mapeamento dos tipos de solo de Niterói (essencial para analisar a porosidade e capacidade de retenção de água).
* `vege_area_mu_3303302.zip` — **Vegetação:** Tipos de cobertura vegetal e uso do solo (importante para modelar a estabilização das encostas pelas raízes).

#### Como obter estes dados?
Os dados originais estão disponíveis gratuitamente no site oficial:
 [https://geoftp.ibge.gov.br/informacoes_ambientais/](https://geoftp.ibge.gov.br/informacoes_ambientais/)
