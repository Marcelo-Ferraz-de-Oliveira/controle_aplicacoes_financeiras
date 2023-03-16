# -*- coding: utf-8 -*-
"""
Este módulo extrai as operaçãoes das notas de corretagem

Suporta atualmente as corretoras:
Clear
XP
Genial

Será gerado um json no seguinte formato:

[
  {
    "nota": 0000,
    "folha": 0,
    "data": "01/01/2001",
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
import copy


def extrair_dados(file_to_open, passwd=""):
    """    Função principal que retorna uma lista de dataframes ou jsons com
    planilha de cabeçalho, negócios e custos de cada nota de corretagem 

    Args:
        file_to_open (_type_): _description_
        passwd (_type_): _description_

    Raises:
        ValueError: _description_
        ValueError: _description_

    Returns:
        _type_: _description_
    """    
    #Verifica qual a corretora antes de continuar
    if not (file_to_open): raise ValueError("Arquivo não informado")
    
    corretora = definir_corretora(file_to_open, passwd)

    #Seleciona as áreas de análise do PDF para cada corretora
    if corretora in ('Clear','XP'):
        area_headers = [0,70,8,100]
        area_negocios = [28,0,53,100]
        area_custos = [53,50,95,100]
        colunas_custos=[450,550,600]
        campos_custos = [2,4,6,9,12,18]
    elif corretora == 'Genial':
        area_headers = [0,70,8,100]
        area_negocios = [25,0,53,100]
        area_custos = [53,50,85,100]
        colunas_custos=[450,560,800]
        campos_custos = [2,4,6,9,11,16]
    else:
        raise ValueError("Corretora não suportada"+corretora)
    #Extração
    headers = extrair_header(file_to_open, passwd, corretora, area_headers)
    negocios = extrair_negocios(file_to_open,passwd, area_negocios)
    custos = extrair_custos(file_to_open,passwd, area_custos, colunas_custos, campos_custos)
    
    return organizar(
        headers, 
        negocios,
        custos)

def str_to_br_currency(string: str) -> str:
    """_summary_

    Args:
        string (str): _description_

    Raises:
        ValueError: _description_

    Returns:
        str: _description_
    """  
    if type(string) is not str:
        raise ValueError('Não foi passada uma string para conversão em moeda!')
    string = string.replace('.','')
    string = string.replace(',','.')
    return string

def definir_corretora(file_to_open: str, passwd: str) -> str:
    """Verify exchange name on file header

    Args:
        file_to_open (str): _description_
        passwd (str): _description_

    Raises:
        FileNotFoundError: _description_
        ValueError: _description_
        ValueError: _description_
        IndexError: _description_
        ValueError: _description_
        ValueError: _description_

    Returns:
        str: _description_
    """
    area_headers = [0,0,28,50]
    try:
        df_corretora = json.dumps(tabula.read_pdf(file_to_open, pages = 1, area=area_headers, stream = True, relative_area= True, password = passwd, output_format='json'))
    except:
        raise FileNotFoundError("Não foi possível abrir o documento. O arquivo não é um PDF ou senha está incorreta.")
    if (df_corretora.find('NOTA DE') == -1):
        raise ValueError("Este documento não é uma nota de negociação.")
    if (df_corretora.find('genial') != -1):
        return 'Genial'
    elif (df_corretora.find('xp') != -1):
        return 'XP'
    elif (df_corretora.find('clear') != -1):
        return 'Clear'
    raise ValueError("Corretora não suportada.")


def organizar(headers: list, negocios: list, custos: list) -> list:
    """Compõe o JSON (dicionário) com 

    Args:
        headers (list): _description_
        negocios (list): _description_
        custos (list): _description_

    Raises:
        IndexError: _description_

    Returns:
        list: _description_
    """  
    if not len(headers) == len(negocios) == len(custos):
        raise IndexError("headers, negócios e custos em quantidades diferentes. Os dados não foram extraídos corretamente!")  
    notas = []
    headers, negocios, custos = agrupar_paginas(headers, negocios, custos)
    #Monta o dicionário com os dados de cada nota e seus negócios e custos correspondentes
    for n, _ in enumerate(headers):        
        headers[n].update({'negocios': negocios[n], 'custos': custos[n]})
        notas.append(headers[n])
    return notas

def agrupar_paginas(headers: list, negocios: list, custos: list) -> tuple:
    """  Verifica se há notas com várias páginas.
    Compara a nota com a nota anterior e, se o código for igual "campo nota",
    agrupa seus negócios e mantém apenas a última página (a que possui a soma dos custos)

    Args:
        headers (list): _description_
        negocios (list): _description_
        custos (list): _description_

    Returns:
        list: _description_
    """
    for n, _ in enumerate(headers):
        if headers[n-1:n]:
            if headers[n]['nota'] == headers[n-1]['nota']:
                #Reindex the index keys to continue after last key of previous negocios
                for key, _ in enumerate(negocios[n]):
                    negocios[n][key]['index'] += negocios[n-1][-1]['index'] + 1
                negocios[n-1].extend(negocios[n])
                negocios[n] = negocios[n-1]
                del negocios[n-1]
                del custos[n-1]
                del headers[n-1]
    return (headers, negocios, custos,)

def extrair_header(file_to_open: str, passwd: str, corretora: str, area_headers: list) -> list:
    """_summary_

    Args:
        file_to_open (str): _description_
        passwd (str): _description_
        corretora (str): _description_
        area_headers (list): _description_

    Returns:
        list: _description_
    """  
    RE_FINDALL_HEADER_STRING = r'^(\d+) (\d+) (.+)$'
    #Extração do número da nota, folha e header
    dfs_header = tabula.io.read_pdf(file_to_open, stream = True, area=area_headers, pages = 'all',relative_area= True, password = passwd, columns=[0])
    #Correção e mudança de nome dos campos
    headers = []
    for df_header in dfs_header:
        list_header = []
        for header in df_header.iloc[:,1]:
            list_header.extend(re.findall(RE_FINDALL_HEADER_STRING, header))
        df_header: pd.DataFrame = pd.DataFrame(list_header)
        df_header.columns = ['nota','folha','data']
        df_header[['nota','folha']] = df_header[['nota','folha']].astype(int)
        df_header['corretora'] = corretora
        headers.extend(df_header.to_dict(orient='records'))
    return headers

def identificar_daytrade(obs: str):
  obs = str(obs)
  if obs[0] == 'D': return 'D'
  return ''

def extrair_negocios(file_to_open: str, passwd: str, area_negocios: list) -> list: 
    """_summary_

    Args:
        file_to_open (str): _description_
        passwd (str): _description_
        area_negocios (list): _description_

    Returns:
        list: _description_
    """  
    RE_FINDALL_NEGOCIO_STRING = r'^(.{1} )?(\d{1}-[A-Z]+) (\w{1}) (OPCAO ?[A-Z ]+|VISTA) (\d\d\/\d\d)? ?((.*) (.*)) ([\d\,\.]+) ([\d\,\.]+) ([\d\,\.]+) (.$)'
    #Extração dos negócios realizados
    dfs_negocios = tabula.io.read_pdf(file_to_open, stream = True, area=area_negocios, pages = 'all',relative_area= True, password = passwd, columns=[0])
    #Usa a expressão regular para dividir os campos, insere no Dataframe e calcula outras colunas
    negocios = []
    for df_negocios in dfs_negocios:
        list_negocios = []
        for negocio in df_negocios.iloc[:,1]:
            list_negocios.extend(re.findall(RE_FINDALL_NEGOCIO_STRING,str_to_br_currency(negocio)))
        df_negocios: pd.DataFrame = pd.DataFrame(list_negocios)
        df_negocios.columns = ['q','negociacao','cv','tipo_mercado','prazo','nome_pregao','___','obs','quantidade','preco','valor_operacao','dc']
        df_negocios = df_negocios.drop(columns=['___'])
        df_negocios['obs'] = df_negocios['obs'].apply(identificar_daytrade)
        df_negocios[['quantidade','preco','valor_operacao']] = df_negocios[['quantidade','preco','valor_operacao']].astype(float)
        df_negocios['codigo'] = df_negocios['nome_pregao'].apply(nome_pregao_to_codigo)
        #calcula o peso percentual nos custos de corretagem
        df_negocios['custo_proporcional'] = df_negocios['valor_operacao'].apply(lambda x: abs(x))/sum(df_negocios['valor_operacao'].apply(lambda x: abs(x)))
        df_negocios = df_negocios.reset_index()
        negocios.append(list(df_negocios.to_dict(orient='index').values()))
    return negocios


def extrair_custos(file_to_open: str, passwd: str, area_custos: list, columns_custos: list, campos: list) -> list:
    """_summary_

    Args:
        file_to_open (str): _description_
        passwd (str): _description_
        area_custos (str): _description_
        columns_custos (list): _description_
        campos (list): _description_

    Returns:
        list: _description_
    """    
    #Extração da planilha de custos da nota
    dfs_custos = tabula.io.read_pdf(file_to_open, stream = True, area=area_custos, pages = 'all',relative_area= True, password = passwd, columns=columns_custos)
    #Seleção dos campos necessários, mudança de nome e inclusão de valores faltantes
    custos = []
    for df_custos in dfs_custos:
        campos_custos= ((df_custos[campos[0]:campos[1]],df_custos[campos[2]:campos[3]],df_custos[campos[4]:campos[5]]))
        df_custos: pd.DataFrame = pd.concat(campos_custos)
        df_custos.columns=['custo','valor','cd']
        df_custos['valor'] = df_custos['valor'].fillna('0').apply(str_to_br_currency).astype(float)
        df_custos = df_custos.set_index('custo').drop('cd', axis=1)
        df_custos = df_custos.transpose()
        df_custos['total'] = round(sum(set(df_custos.loc['valor'].values)),2)
        custos.extend(df_custos.to_dict(orient='records'))
    return custos



  