"""
Obtém o CSV com todos os ativos listados na B3 no dia
Trata-se de um arquivo obtido através de um botão na página (não há link direto),
por isso é necessário fazer scraping da página para clicar no botão e fazer o download
"""

from webapp.headless_webdriver import get_headless_selenium_webdriver
import time
import pandas as pd
from datetime import date, timedelta
import glob
import re
import json
import os

def get_wd(dat):
    URL_B3_INSTRUMENTS = 'https://arquivos.b3.com.br/tabelas/InstrumentsConsolidated/'+dat.strftime("%Y-%m-%d")
    wd = get_headless_selenium_webdriver()
    wd.get(URL_B3_INSTRUMENTS)
    time.sleep(1)
    #verifica se é feriado ou fim de semana e tenta no dia anterior 
    if wd.find_elements('id','label-nao-encontrado'):
        return get_wd(dat-timedelta(days=1))
    return wd

def obter_CSV_B3():
    #Não há listagem em finais de semana
    wd = get_wd(date.today())    
    #Seleciona o último link e clica nele para baixar o arquivo
    #Não há id, classe, ou qualquer outra coisa para identificar o link!
    links = wd.find_elements('tag name','a')
    links[-1].click()
    time.sleep(3)
    #Retorna um Dataframe e remove o arquivo
    files = glob.glob('Instruments*.csv')
    for file in files:
        if 'Instruments' in file:
            print(file)
            df = pd.read_csv(file,sep=';',encoding='ISO-8859-1', low_memory=False)
            os.remove(file)
            return df
    return pd.DataFrame()
    
if __name__ == "__main__":
    #Obter a lista de códigos (ON, PN, ETC) e o seu código correspondente (3, 4, ETC)
    resultado = obter_CSV_B3()[['TckrSymb','SpcfctnCd']]
    resultado['TckrSymb'] = resultado['TckrSymb'].dropna().apply(lambda x: re.sub(r'^\w*[^0-9]{1,2}',r'',x))
    resultado = resultado.drop(resultado[resultado['TckrSymb'] == ""].index)
    resultado['SpcfctnCd'] = resultado['SpcfctnCd'].dropna().apply(lambda x: x.replace(" ", ""))
    resultado = resultado.drop_duplicates(subset=['SpcfctnCd']).sort_values('TckrSymb')
    with open('codigos_b3_tipos.json','w') as f:
        json.dump(resultado.set_index('SpcfctnCd').to_dict(orient='dict'), f)    