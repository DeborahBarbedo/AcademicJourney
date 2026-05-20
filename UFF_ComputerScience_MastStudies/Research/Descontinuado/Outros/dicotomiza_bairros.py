from unidecode import unidecode 
import psycopg2

sql_bairro = '''
            SELECT DISTINCT bairro
            FROM vw_ocorrencia_deslizamento_chuva
'''

def get_sql_dicotomizacao(string_bairros):
    sql_dicotomizacao = f'''
                CREATE OR REPLACE VIEW public.vw_ocorrencia_deslizamento_chuva AS
                    select vac.indice_pluv
                        ,vac.quinzemin
                        ,vac.trintamin
                        ,vac.umahora
                        ,vac.seishoras
                        ,vac.dozehoras
                        ,vac.vintequatrohoras
                        ,vac.quarentaoitohoras
                        ,vac.setentaduashoras
                        ,vac.noventaseishoras
                        ,vac.mes
                        ,vac.status_indice_pluv
                        ,vac.status_quinzemin
                        ,vac.status_trintamin
                        ,vac.status_umahora
                        ,vac.status_seishoras
                        ,vac.status_dozehoras
                        ,vac.status_vintequatrohoras
                        ,vac.status_quarentaoitohoras
                        ,vac.status_setentaduashoras
                        ,vac.status_noventaseishoras
                        ,vac.status_mes
                        ,vac.tempo
                        ,vac.id_estacao
                        ,vac.bairro
                        ,vaod.ocorrencia
                        ,vaod.ameaca_prevencao
                        ,vaod.mapeamento
                        ,vaod.qtd_solicitacoes
                        ,vaod.latitude  
                        ,vaod.long  
                        {string_bairros}    
                    from vw_aux_chuva vac
                    left join vw_aux_ocorrencia_deslizamento vaod 
                    on vac.id_tempo = vaod.id_tempo
                    where  ( vac.id_estacao=(select id_estacao
                                            from voronoi as von
                                            where (vaod.latitude between von.lat and von.lat+0.00216217392)
                                            and(vaod.long between von.long and von.long+0.00306718)))
                '''
    return sql_dicotomizacao

def create_string_case_bairros(bairros):
    
    #eliminando espaços e caracteres especiais dos nomes dos bairros
    col_names = [unidecode(bairro).replace(" ", "_").replace("'","") for bairro in bairros]

    str = ''
    for i in range(len(bairros)):
        if bairros[i] != "PONTA D'AREIA": #nomes com caracter especial tem que ter tratamento
            aux = f''',case when vac.bairro='{bairros[i]}' then 1 else 0 end as "{col_names[i]}"'''
        else: 
            aux = f''',case when vac.bairro='PONTA D''AREIA' then 1 else 0 end as "{col_names[i]}"'''
        str += aux

    return str


def job(database, user, password, host, port):
    conn = psycopg2.connect(database=database, user=user, password=password, host=host, port=port)

    with conn.cursor() as cursor:
        
        print("INICIANDO DICOTOMIZACAO")

        #pega os bairros presentes na view
        cursor.execute(sql_bairro)
        bairros = list(map(lambda tup: tup[0], cursor.fetchall()))

        #cria a string que representam os casos dicotomizados para cada bairro
        case_bairros = create_string_case_bairros(bairros)

        #atualiza a view
        sql_dicotomizacao = get_sql_dicotomizacao(case_bairros)
        cursor.execute(sql_dicotomizacao)

        conn.commit()

        print("FIM DA DICOTOMIZACAO")

if __name__ == '__main__':

    #substituir aqui as variaveis
    database = ''
    user = ''
    password = ''
    host = ''
    port = ''

    job(database, user, password, host, port)