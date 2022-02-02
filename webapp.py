import extrator
import json
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/negocios')
def get_negocios():
    arquivo = request.args.get('arquivo')
    senha = request.args.get('senha')
    return extrator.extrair_dados(arquivo, senha) 
