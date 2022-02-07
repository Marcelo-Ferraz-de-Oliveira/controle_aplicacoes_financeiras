# -*- coding: utf-8 -*-

#Este módulo extrai as operaçãoes das notas de corretagem
#Suporta atualmente as corretoras:
#Clear
#XP
#Genial


#!pip install tabula-py
#!apt install default-jre
import tabula
import pandas as pd
import json
from tradutor import nome_pregao_to_codigo

def traduzir_acao(string):
  return 


def str_to_br_currency(string):
  #Write description
  if type(string) != type('string'):
    raise ValueError('Não foi passada uma string para conversão em moeda!')
  string = string[::-1]
  string = string.replace('.','')
  string = string.replace(',','.',1)
  string = string.replace(',','')
  string = string[::-1]
  return float(string)

def us_currency_to_float(n):
  #Write description
  #Números com 2 ou mais pontos (pandas vai converter pra string)
  if type(n) == str:
    return float(n.replace('.',''))
  #Números com 1 ponto
  elif n == int(n):
    return float(n)
  else: 
    return float(n*1000)

def fix_sep_negocios(df):
  word_df = df.copy()
  word_df['Preço'] = word_df['Preço'].apply(str_to_br_currency)
  word_df['Valor Operação'] = word_df['Valor Operação'].apply(str_to_br_currency)
  word_df['Quantidade'] = word_df['Quantidade'].apply(us_currency_to_float)
  return word_df

def fix_sep_custos(df):
#Write description
  word_df = df.copy()
  word_df['Valor'] = word_df['Valor'].apply(str_to_br_currency)
  return word_df

def definir_corretora(file_to_open, passwd):
# Write description
# Verifica qual o nome da corretora no cabeçalho da nota
  area_header = [0,0,28,50]
  try:
    df_corretora = json.dumps(tabula.read_pdf(file_to_open, pages = 1, area=area_header, stream = True, relative_area= True, password = passwd, output_format='json'))
  except:
    raise ValueError("Erro ao abrir o arquivo informado")
  if (df_corretora.find('NOTA DE') == -1):
    raise ValueError("Documento inválido.")
  if (df_corretora.find('genial') != -1):
    return 'genial'
  elif (df_corretora.find('xp') != -1):
    return 'xp'
  elif (df_corretora.find('clear') != -1):
    return 'clear'
  raise ValueError("Corretora não suportada.")

#Ativa as mensagens na console (dados da nota durante o processamento)
debug = False

def organizar(datas, negocios, custos):
# """
# Organiza cada data com seus respectivos negócios e planilhas de custos
# """
  if not len(datas) == len(negocios) == len(custos):
    raise ValueError("Datas, negócios e custos em quantidades diferentes. Os dados não foram extraídos corretamente!")  
  var = {}
  #print(datas)
  for n in range(0,len(datas)):
    if debug: print([datas[n],negocios[n], custos[n]])
    datas[n][0].update({'Negocios': negocios[n], 'Custos': custos[n][0]})
    var['Nota '+ str(n+1)] = datas[n][0]
  return var

def extrair_data(file_to_open, passwd, formato, corretora, area_datas):
# """
# Write description
# """  

  #Extração do número da nota, folha e data
  df_datas = tabula.io.read_pdf(file_to_open, stream = True, area=area_datas, pages = 'all',relative_area= True, password = passwd)
  if debug: print(df_datas)
  #Correção e mudança de nome dos campos
  df_datas_c = []
  for content in df_datas:
    if 'Unnamed: 0' in content.columns:
      content = content[['Nr. nota','Unnamed: 0','Data pregão']]
    content.columns = ['nr. nota','folha','data']
    content['corretora'] = corretora
    #content = content.reset_index()    
    if formato == 'json': content = content.to_dict(orient='records')
    df_datas_c.append(content)
  if debug: print(df_datas_c)
  return df_datas_c

def extrair_negocios(file_to_open, passwd, formato, corretora, area_negocios):
# """
# Write description
# """  
  #Extração dos negócios realizados
  df_negocios = tabula.io.read_pdf(file_to_open, stream = True, area=area_negocios, pages = 'all',relative_area= True, password = passwd)
  if debug: print(df_negocios)
  #Exclui associações incorretas (NANs) e colunas desnecessárias, renomeia colunas e corrige os separadores numéricos
  df_negocios_c = []
  for content in df_negocios:
    content = content.dropna(axis=1, how='any')
    if content['Tipo mercado'][0] == 'OPCAO DE COMPRA':
      content = content.drop(['Prazo','Unnamed: 0'], axis = 1)
      content.columns = ['Negociação','C/V','Tipo de mercado','Nome Pregão','Quantidade','Preço','Valor Operação','D/C']
    elif content['Tipo mercado'][0] == 'VISTA':
      content.columns = ['Negociação','C/V','Tipo de mercado','Nome Pregão','Quantidade','Preço','Valor Operação','D/C']
    else: continue
    #content = content.reset_index()
    content = fix_sep_negocios(content)
    content['Código'] = content['Nome Pregão'].apply(nome_pregao_to_codigo)
    if formato == 'json': content = content.to_dict(orient='index')
    df_negocios_c.append(content)
  return df_negocios_c

def extrair_custos(file_to_open, passwd, formato, corretora, area_custos, columns_custos, campos):
# """
# Write description
# """  
    #Extração da planilha de custos da nota
    df_custos = tabula.io.read_pdf(file_to_open, stream = True, area=area_custos, pages = 'all',relative_area= True, password = passwd, columns=columns_custos)
    if debug: print(df_custos)
    #Seleção dos campos necessários, mudança de nome e inclusão de valores faltantes
    df_custos_c = []
    for content in df_custos:
      campos_custos= ((content[campos[0]:campos[1]],content[campos[2]:campos[3]],content[campos[4]:campos[5]]))
      content = pd.concat(campos_custos)
      content.columns=['Custo','Valor','C/D']
      content['Valor'] = content['Valor'].fillna('0')
      #content['C/D'] = content['C/D'].fillna('N/A')
      content = content.set_index('Custo').drop('C/D', axis=1)
      content = fix_sep_custos(content)
      content = content.transpose()
      if formato =='json': content = content.to_dict(orient='records')
      df_custos_c.append(content)
    return df_custos_c

def extrair_dados(file_to_open, passwd, formato = 'json'):
  # """
  # Write description
  # """ 
  #Função principal que retorna uma lista de dataframes ou jsons com
  #planilha de cabeçalho, negócios e custos de cada nota de corretagem 

  #Verifica qual a corretora antes de continuar
  if not (file_to_open): raise ValueError("Arquivo não informado")
  
  corretora = definir_corretora(file_to_open, passwd)
  if debug: print(corretora)

  #Seleciona as áreas de análise do PDF para cada corretora
  if corretora in ('clear','xp'):
    area_datas = [0,70,8,100]
    area_negocios = [28,0,53,100]
    area_custos = [53,50,95,100]
    colunas_custos=[450,550,600]
    campos_custos = [2,4,6,9,12,18]
  elif corretora == 'genial':
    area_datas = [0,70,8,100]
    area_negocios = [25,0,53,100]
    area_custos = [53,50,85,100]
    colunas_custos=[450,560,800]
    campos_custos = [2,4,6,9,11,16]
  else:
    raise ValueError("Corretora não suportada"+corretora)


  #Extração
  df_datas_c = extrair_data(file_to_open, passwd, formato, corretora, area_datas)
  df_negocios_c = extrair_negocios(file_to_open,passwd, formato, corretora, area_negocios)
  df_custos_c = extrair_custos(file_to_open,passwd, formato, corretora, area_custos, colunas_custos, campos_custos)
  
  return organizar(
    df_datas_c, 
    df_negocios_c,
    df_custos_c)



if __name__ == "__main__":
  pass