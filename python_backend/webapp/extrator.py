# -*- coding: utf-8 -*-

#Este módulo extrai as operaçãoes das notas de corretagem
#Suporta atualmente as corretoras:
#Clear
#XP
#Genial

"""
Será gerado um json no seguinte formato:

[
  {
    "nota": 0000,
    "folha": 0,
    "data": 01/01/2001,
    "corretora": "nome_corretora",
    "negocios": [
      {
        "index": 0,
        "negociacao": "1-BOVESPA",
        "cv": "C",
        "tipo_mercado": "VISTA",
        "nome_pregao": "PETROBRASONN2"
        "quantidade": 100,
        "preco": 20.0,
        "valor_operacao": 2000.0,
        "dc": "C",
        "codigo": "PETR4"
      },
      {
        "index": 1,
        "negociacao": "1-BOVESPA",
        "cv": "C",
        "tipo_mercado": "VISTA",
        "nome_pregao": "PETROBRASONN2"
        "quantidade": 100,
        "preco": 20.0,
        "valor_operacao": 2000.0,
        "dc": "C",
        "codigo": "PETR4"
      }],
    "custos": {
      "taxa_liquidacao": 0.0,
      "taxa_registro": 0.0,
      "taxa_termo_opcoes": 0.0,
      #Outras taxas, a depender da corretora
      "total": 0.0
      
    }
  }
]
"""
import tabula
import pandas as pd
import json
from webapp.tradutor import nome_pregao_to_codigo
import re

def traduzir_acao(string):
  return 

def str_to_br_currency(string):
  #Write description
  if type(string) is not str:
    raise ValueError('Não foi passada uma string para conversão em moeda!')
  string = string[::-1]
  string = string.replace('.','')
  string = string.replace(',','.',1)
  string = string.replace(',','')
  string = string[::-1]
  return float(string)
  
def fix_sep_custos(df):
  word_df = df.copy()
  word_df['valor'] = word_df['valor'].apply(str_to_br_currency)
  return word_df

def definir_corretora(file_to_open, passwd):
# Verifica qual o nome da corretora no cabeçalho da nota
  area_header = [0,0,28,50]
  try:
    df_corretora = json.dumps(tabula.read_pdf(file_to_open, pages = 1, area=area_header, stream = True, relative_area= True, password = passwd, output_format='json'))
  except:
    raise ValueError("Erro ao abrir o arquivo informado")
  if (df_corretora.find('NOTA DE') == -1):
    raise ValueError("Documento inválido.")
  if (df_corretora.find('genial') != -1):
    return 'Genial'
  elif (df_corretora.find('xp') != -1):
    return 'XP'
  elif (df_corretora.find('clear') != -1):
    return 'Clear'
  raise ValueError("Corretora não suportada.")

#Ativa as mensagens na console (dados da nota durante o processamento)
debug = False

def organizar(datas, negocios, custos):
  if not len(datas) == len(negocios) == len(custos):
    raise IndexError("Datas, negócios e custos em quantidades diferentes. Os dados não foram extraídos corretamente!")  
  notas = []
  #Verifica se há notas com várias páginas
  #Compara a nota com a nota anterior e, se o código for igual "campo nota"
  #agrupa seus negócios e mantém apenas a última página (a que possui a soma dos custos) 
  for n, _ in enumerate(datas):
    #Verifica se não é o primeiro item
    if datas[n-1:n]:
      if datas[n]['nota'] == datas[n-1]['nota']:
        negocios[n].extend(negocios[n-1])
        del negocios[n-1]
        del custos[n-1]
        del datas[n-1]
  #Monta o dicionário com os dados de cada nota e seus negócios e custos correspondentes
  for n, _ in enumerate(datas):        
    datas[n].update({'negocios': negocios[n], 'custos': custos[n]})
    notas.append(datas[n])
  return notas

def extrair_data(file_to_open, passwd, corretora, area_datas, columns_data):
  #Extração do número da nota, folha e data
  dfs_data = tabula.io.read_pdf(file_to_open, stream = True, area=area_datas, pages = 'all',relative_area= True, password = passwd, columns=columns_data)
  #Correção e mudança de nome dos campos
  datas = []
  for df_data in dfs_data:
    if 'Unnamed: 0' in df_data.columns:
      df_data = df_data[['Nr. nota','Unnamed: 0','Data pregão']]
    df_data.columns = ['nota','folha','data']
    df_data['corretora'] = corretora
    datas.extend(df_data.to_dict(orient='records'))
  if debug: print(datas)
  return datas

def extrair_negocios(file_to_open, passwd, corretora, area_negocios, columns_negocios=[0]): 
  
  RE_FINDALL_NEGOCIO_STRING = r'^(.{1} )?(\d{1}-[A-Z]+) (\w{1}) (OPCAO [A-Z ]+|VISTA) (\d\d\/\d\d)? ?(.*) (.{1} )?([\d\,\.]+) ([\d\,\.]+) ([\d\,\.]+) (.$)'
  #Extração dos negócios realizados
  dfs_negocios = tabula.io.read_pdf(file_to_open, stream = True, area=area_negocios, pages = 'all',relative_area= True, password = passwd, columns=columns_negocios)
  #Usa a expressão regular para dividir os campos, insere no Dataframe e calcula outras colunas
  negocios = []
  for df_negocios in dfs_negocios:
    list_negocios = []
    for negocio in df_negocios.iloc[:,1]:
      list_negocios.extend(re.findall(RE_FINDALL_NEGOCIO_STRING,negocio.replace(".","").replace(",",".")))
    df_negocios = pd.DataFrame(list_negocios)
    df_negocios.columns = ['q','negociacao','cv','tipo_mercado','prazo','nome_pregao','obs','quantidade','preco','valor_operacao','dc']
    df_negocios[['quantidade','preco','valor_operacao']] = df_negocios[['quantidade','preco','valor_operacao']].astype(float)
    df_negocios['codigo'] = df_negocios['nome_pregao'].apply(nome_pregao_to_codigo)
    #calcula o peso percentual nos custos de corretagem
    df_negocios['custo_proporcional'] = df_negocios['valor_operacao'].apply(lambda x: abs(x))/sum(df_negocios['valor_operacao'].apply(lambda x: abs(x)))
    df_negocios = df_negocios.reset_index()
    negocios.append(list(df_negocios.to_dict(orient='index').values()))
  return negocios


def extrair_custos(file_to_open, passwd, corretora, area_custos, columns_custos, campos):
    #Extração da planilha de custos da nota
    dfs_custos = tabula.io.read_pdf(file_to_open, stream = True, area=area_custos, pages = 'all',relative_area= True, password = passwd, columns=columns_custos)
    if debug: print(dfs_custos)
    #Seleção dos campos necessários, mudança de nome e inclusão de valores faltantes
    custos = []
    for df_custos in dfs_custos:
      campos_custos= ((df_custos[campos[0]:campos[1]],df_custos[campos[2]:campos[3]],df_custos[campos[4]:campos[5]]))
      df_custos = pd.concat(campos_custos)
      df_custos.columns=['custo','valor','cd']
      df_custos['valor'] = df_custos['valor'].fillna('0')
      df_custos = df_custos.set_index('custo').drop('cd', axis=1)
      df_custos = fix_sep_custos(df_custos)
      df_custos = df_custos.transpose()
      df_custos['total'] = round(sum(set(df_custos.loc['valor'].values)),2)
      custos.extend(df_custos.to_dict(orient='records'))
    return custos

def extrair_dados(file_to_open, passwd):
  #Função principal que retorna uma lista de dataframes ou jsons com
  #planilha de cabeçalho, negócios e custos de cada nota de corretagem 

  #Verifica qual a corretora antes de continuar
  if not (file_to_open): raise ValueError("Arquivo não informado")
  
  corretora = definir_corretora(file_to_open, passwd)
  if debug: print(corretora)

  #Seleciona as áreas de análise do PDF para cada corretora
  if corretora in ('Clear','XP'):
    area_datas = [0,70,8,100]
    colunas_datas = [465,500]
    area_negocios = [28,0,53,100]
    #colunas_negocios = [40,85,101,160,193,305,360,410,460,540]
    colunas_negocios = [0]
    
    area_custos = [53,50,95,100]
    colunas_custos=[450,550,600]
    campos_custos = [2,4,6,9,12,18]
  elif corretora == 'Genial':
    area_datas = [0,70,8,100]
    area_negocios = [25,0,53,100]
    area_custos = [53,50,85,100]
    colunas_custos=[450,560,800]
    campos_custos = [2,4,6,9,11,16]
  else:
    raise ValueError("Corretora não suportada"+corretora)
  #Extração
  datas = extrair_data(file_to_open, passwd, corretora, area_datas, colunas_datas)
  negocios = extrair_negocios(file_to_open,passwd, corretora, area_negocios, colunas_negocios)
  custos = extrair_custos(file_to_open,passwd, corretora, area_custos, colunas_custos, campos_custos)
  
  return organizar(
    datas, 
    negocios,
    custos)

  