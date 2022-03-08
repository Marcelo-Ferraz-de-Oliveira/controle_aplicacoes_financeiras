from webapp.extrator import extrair_dados
import json
from flask import Flask, request, jsonify
import string
import random
from os import remove
from webapp.position import Position, atualizar_posicao
from webapp.profit import Profit
from datetime import datetime

app = Flask(__name__)
app.config['TRAP_HTTP_EXCEPTIONS']=True


position: Position = Position()
profit: Profit = Profit()

@app.route('/monthprofit', methods=['POST'])
def get_month_profit() -> str:
    return json.dumps(profit.get_month_profit(datetime(2022, 2, 1)))

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
        position.position = atualizar_posicao(position.position, json.loads(request.values["nota"]))
        position.liquidate_expired_option()
        profit.update_profit(position)
    return json.dumps(position.position)           
    
@app.route('/negocios', methods=['POST'])
def get_negocios_post():
    # try:
    if request.files:
        return json.dumps(
            process_multiple_files(
                request.files.values(), 
                request.values['pwd']))
    else:
        return json.dumps([])
    # except Exception as e:
    #     return str(e), 500

@app.errorhandler(Exception)
def handle_server_error(e):
    return str(e), 206

def process_multiple_files(files, password) -> list:
    notas = []
    for file in files:
        temp_file = random_tempfile()
        file.save(temp_file)
        notas.extend(extrair_dados(temp_file, password))
        remove(temp_file)
    return notas
    
def random_tempfile() -> str:
    return f"/tmp/{''.join(random.choice(string.ascii_letters) for x in range(30))}"


if __name__ == "__main__":
    app.run()