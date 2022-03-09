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

app = Flask(__name__)
app.config['TRAP_HTTP_EXCEPTIONS']=True


position: Position = Position()
profit: Profit = Profit()
notas: Notas = Notas()

@app.route('/monthprofit', methods=['POST'])
def get_month_profit() -> str:
    # return json.dumps(profit.get_month_profit(datetime(2022, 2, 1)))
    if request.values:
        pass
    return json.dumps(profit.get_month_profit(datetime.today()))

@app.route('/somarlucro', methods=['POST'])
def set_lucro() -> str:
    return json.dumps(profit.profit)

@app.route('/lucro', methods=['POST'])
def get_lucro() -> str:    
    return json.dumps(profit.profit)

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
    app.run()