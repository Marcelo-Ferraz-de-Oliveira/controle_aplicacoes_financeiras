from webapp.extrator import extrair_dados
import json
from flask import Flask, request
import string
import random
from os import remove
from webapp.posicoes import atualizar_posicao


app = Flask(__name__)

#posicao = Posição acionária atual        
#Inicia uma posição vazia, enquanto não há um banco de dados
posicao = {}



@app.route('/somarnotas', methods=['POST'])
def set_somarnotas():
    if request.values:
       return atualizar_posicao(posicao, json.loads(request.values["nota"]))
                    
    return json.dumps(posicao)           

@app.route('/posicao', methods=['POST'])
def get_posicao():
    return json.dumps(posicao)

@app.route('/negocios', methods=['GET'])
def get_negocios():
    dados = extrair_dados(
                request.args.get('arquivo'),
                request.args.get('senha')
            )

    return json.dumps(dados)
        
@app.route('/negocios', methods=['POST'])
def get_negocios_post():
    #O arquivo inteiro é passado através do POST
    #e é necessário amazená-lo em um arquivo temporário para posterior processamento
    if request.files:
        #Cria um arquivo temporário com nome aleatório para armazenar o arquivo
        notas = []
        for file in request.files.values():
            temp_file = '/tmp/'+( ''.join(random.choice(string.ascii_letters) for x in range(30)))
            with open(temp_file, 'wb') as f:
                f.write(file.read())
            dados = extrair_dados(
                        temp_file,
                        request.values['pwd']
                    )
            remove(temp_file)
            notas += dados
        return json.dumps(notas)
    else:
        return json.dumps([])


if __name__ == "__main__":
    app.run()