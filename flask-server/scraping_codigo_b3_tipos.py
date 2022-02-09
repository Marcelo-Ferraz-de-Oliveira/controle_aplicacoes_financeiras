# !apt install chromium-chromedriver
# !cp /usr/lib/chromium-browser/chromedriver /usr/bin
# !pip install selenium


#Obtém o CSV com todos os ativos listados na B3 no dia
#Trata-se de um arquivo obtido através de um botão na página (não há link direto),
#por isso é necessário fazer scraping da página para clicar no botão e fazer o download

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd
from datetime import date
import glob
import os
import re
import json

def obter_CSV_B3():
    file = glob.glob('Instruments*.csv')[0]
    if 'Instruments' in file:
        df = pd.read_csv(file,sep=';',encoding='ISO-8859-1', low_memory=False)
        #os.remove(file)
        return df
    else:
        options = webdriver.ChromeOptions()
        #Opções para usar navegador sem interface gráfica
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--enable-javascript')
        #Define o diretório padrão para download como o diretório atual
        prefs = {"download.default_directory" : "."}
        options.add_experimental_option('prefs',prefs)
        
        url_b3 = 'https://arquivos.b3.com.br/tabelas/InstrumentsConsolidated/'+date.today().strftime("%Y-%m-%d")

        wd = webdriver.Chrome('chromedriver',options=options)
        wd.get(url_b3)
        time.sleep(1)
        #Seleciona o último link e clica nele para baixar o arquivo
        #Não há id, classe, ou qualquer outra coisa para identificar o link!
        links = wd.find_elements('tag name','a')
        links[-1].click()
        time.sleep(3)

        #Retorna um Dataframe e remove o arquivo
        file = glob.glob('Instruments*.csv')[0]
        df = pd.read_csv(file,sep=';',encoding='ISO-8859-1', low_memory=False)
        os.remove(file)
        return df
    
if __name__ == "__main__":
    #print(sorted(set(list(map(lambda x: re.sub(r' +',' ',x),obter_CSV_B3()['SpcfctnCd'].dropna().unique())))))
    #Obter a lista de códigos (ON, PN, ETC) e o seu código correspondente (3, 4, ETC)
    #https://www.b3.com.br/data/files/88/57/AB/07/D7A6E610B60806E6AC094EA8/Cadastro%20de%20Instrumentos%20_Listados_.pdf
    resultado = obter_CSV_B3()[['TckrSymb','SpcfctnCd']]
    resultado['TckrSymb'] = resultado['TckrSymb'].dropna().apply(lambda x: re.sub(r'^\w*[^0-9]{1,2}',r'',x))
    resultado = resultado.drop(resultado[resultado['TckrSymb'] == ""].index)
    resultado['SpcfctnCd'] = resultado['SpcfctnCd'].dropna().apply(lambda x: x.replace(" ", ""))
    resultado = resultado.drop_duplicates(subset=['SpcfctnCd']).sort_values('TckrSymb')
    #resultado.set_index('SpcfctnCd').to_csv('codigos_b3.csv')
    with open('codigos_b3_tipos.json','w') as f:
        json.dump(resultado.set_index('SpcfctnCd').to_dict(orient='dict'), f)    