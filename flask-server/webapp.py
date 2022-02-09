from extrator import extrair_dados
import json
from flask import Flask, request
from json2html import *

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
    tempfile = '/tmp/tempfile'
    with open(tempfile, 'wb') as f:
        f.write(request.files['file'].read())
    dados = extrair_dados(
                tempfile,
                request.values['pwd']
            )
    

    #dados["Nota 1"]['Custos']['Total'] = 
    #print(json.dumps(calcular_total(dados)))
    return json.dumps(calcular_total(dados))
    #return json.dumps(dados)
    
