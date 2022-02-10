from extrator import extrair_dados
import json
from flask import Flask, request
from json2html import *
import string
import random
from os import remove


app = Flask(__name__)

def template (content):
    return '<!DOCTYPE html> <html lang="en"> <head> <meta charset="UTF-8"> <meta name="viewport" content="width=device-width, initial-scale=1.0">   <title>Bootstrap Site</title>   <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/5.0.0-alpha1/css/bootstrap.min.css" integrity="sha384-r4NyP46KrjDleawBgD5tp8Y7UzmLA05oM1iAEQ17CSuDqnUK2+k9luXQOfXJCJ4I" crossorigin="anonymous">   <script src="https://cdn.jsdelivr.net/npm/popper.js@1.16.0/dist/umd/popper.min.js" integrity="sha384-Q6E9RHvbIyZFJoft+2mJbHaEWldlvI9IOYy5n3zV9zzTtmI3UksdQRVvoxMfooAo" crossorigin="anonymous"></script> <script src="https://stackpath.bootstrapcdn.com/bootstrap/5.0.0-alpha1/js/bootstrap.min.js" integrity="sha384-oesi62hOLfzrys4LxRF63OJCXdXDipiYWBnvTl9Y9/TRlw5xlKIEHpNyvvDShgf/" crossorigin="anonymous"></script></head><body>' + content + ' </body> </html>' 

def calcular_total (dados):
    for nota, _ in enumerate(dados):
        dados[nota]['Custos']['Total'] = 0
        for custo in dados[nota]['Custos']:
            if custo != 'Total': dados[nota]['Custos']['Total'] += dados[nota]['Custos'][custo]
    return dados

#Une os dados de notas com múltiplas páginas
# def comparar_paginas(dados):
#     nrnota = []
#     for nota in dados:
#         nrnota.append(nota['nr. nota'])
    

# def unir_paginas(dados):
#     pass
        

@app.route('/negocios', methods=['GET'])
def get_negocios():
    dados = extrair_dados(
                request.args.get('arquivo'),
                request.args.get('senha')
            )

    #dados["Nota 1"]['Custos']['Total'] = 
    #print(json.dumps(calcular_total(dados)))
    return json.dumps(calcular_total(dados))
    #return json.dumps(dados)
        
@app.route('/negocios', methods=['POST'])
def get_negocios_post():
    #O arquivo inteiro é passado através do POST
    #e é necessário amazená-lo em um arquivo temporário para posterior processamento
    if request.files:
        #Cria um arquivo temporário com nome aleatório para armazenar o arquivo
        temp_file = '/tmp/'+( ''.join(random.choice(string.ascii_letters) for x in range(30)))
        with open(temp_file, 'wb') as f:
            f.write(request.files['file'].read())
        dados = extrair_dados(
                    temp_file,
                    request.values['pwd']
                )
        remove(temp_file)
        return json.dumps(calcular_total(dados))
    else:
        return json.dumps([])

#posicao = {"ABEV3": {"ativo": "ABEV3", "quantidade": 17900, "preco_medio": 14.95},
#           "IRBR3": {"ativo": "IRBR3", "quantidade": 2600, "preco_medio": 3.64}}
posicao = {}


def atualizar_posicao(posicao, notas):
    for i, nota in enumerate(notas):
        for j, negocio in enumerate(nota["Negocios"]):
            if negocio["Código"] in list(posicao.keys()):
                k = negocio["Código"]
                #ma = preço médio anterior
                #qa = quantidade anterior
                #m = preço médio atual (Valor da Operação)
                #q = quantidade atual
                # Novo preço médio = ((ma*qa)+m)/(qa+q)
                p_medio = (((posicao[k]['preco_medio']*posicao[k]['quantidade'])+negocio['Valor Operação'])/(posicao[k]['quantidade']+negocio['Quantidade']))
                posicao[k]['quantidade'] += negocio["Quantidade"]
                posicao[k]['preco_medio'] = p_medio
            else:
                posicao[negocio["Código"]]={
                    "ativo": negocio["Código"],
                    "quantidade": negocio["Quantidade"],
                    "preco_medio": negocio["Valor Operação"]/negocio["Quantidade"]}
    return posicao

@app.route('/somarnotas', methods=['POST'])
def set_somarnotas():
    if request.values:
       return atualizar_posicao(posicao, json.loads(request.values["nota"]))
                    
    return json.dumps(posicao)           

@app.route('/posicao', methods=['POST'])
def get_posicao():
    return json.dumps(posicao)