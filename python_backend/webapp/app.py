from webapp.extrator import extrair_dados
import json
from flask import Flask, request, jsonify
import string
import random
from os import remove
from webapp.position import Position
from webapp.profit import Profit
from webapp.notas import Notas
from datetime import datetime
from webapp.connect_db import get_database

database = get_database()
app = Flask(__name__, static_folder='../../react_frontend/build', static_url_path="/")
app.config['TRAP_HTTP_EXCEPTIONS']=True


position: Position = Position(database)
profit: Profit = Profit()
notas: Notas = Notas(database)

@app.route("/")
def index():
    return app.send_static_file('index.html')

@app.route('/monthprofit', methods=['POST'])
def get_month_profit() -> str:
    if request.values:
        pass
    return json.dumps(profit.month_profit)

@app.route('/monthprofitdaytrade', methods=['POST'])
def get_month_profit_daytrade() -> str:
    if request.values:
        pass
    return json.dumps(profit.month_profit_daytrade)

@app.route('/monthtax', methods=['POST'])
def get_month_tax() -> str:
    if request.values:
        pass
    return json.dumps(profit.month_tax)

@app.route('/monthtaxdaytrade', methods=['POST'])
def get_month_tax_daytrade() -> str:
    if request.values:
        pass
    return json.dumps(profit.month_tax_daytrade)

@app.route('/lucro', methods=['POST'])
def get_lucro() -> str:    
    return json.dumps(profit.profit)

@app.route('/lucrodaytrade', methods=['POST'])
def get_lucro_daytrade() -> str:    
    return json.dumps(profit.profit_daytrade)

@app.route('/posicao', methods=['POST'])
def get_posicao() -> str:
    return json.dumps(position.position)

@app.route('/somarnotas', methods=['POST'])
def set_somarnotas():
    if request.values:
        position.atualizar_posicao(json.loads(request.values["nota"]))
        position.check_expired_options()
        profit.update_profit(position)
    return json.dumps(position.position)           

@app.route('/zerarposicao', methods=['POST'])
def set_zerarposicao():
    if request.values:
        position.liquidate_expired_option(json.loads(request.values["code"]))
        profit.update_profit(position)
    return json.dumps(position.position)

@app.route('/negocios', methods=['POST'])
def get_negocios_post():
    if request.files:
        return json.dumps(
            process_multiple_files(
                request.files.values(), 
                request.values['pwd']).nota)
    else:
        return json.dumps(notas.nota)

@app.errorhandler(Exception)
def handle_server_error(e):
    return str(e), 206

def process_multiple_files(files, password) -> Notas:
    for file in files:
        temp_file = random_tempfile()
        try:
            file.save(temp_file)
            nota = extrair_dados(temp_file, password)
            notas.addNotas(nota)
        finally:
            remove(temp_file)
    return notas
    
def random_tempfile() -> str:
    return f"/tmp/nota_{''.join(random.choice(string.ascii_letters) for x in range(30))}.pdf"


if __name__ == "__main__":
    app.run(host="0.0.0.0")