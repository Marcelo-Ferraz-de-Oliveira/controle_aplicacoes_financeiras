from datetime import datetime, timedelta
import copy
class Position:
    def __init__(self, database) -> None:
        self.__position = database['position']
        if not self.__position.find_one(): self.__position.insert_one({})
        self.__added_notes = database['added_notes']

    @property
    def position(self) -> dict:
        result = self.__position.find_one()
        result = {key: result[key] for key in result if key != "_id"}
        return result
    @position.setter
    def position(self, position: dict) -> None:
        self.__position.find_one_and_replace({}, position) 

    @property
    def added_notes(self) -> list:
        result = self.__added_notes.find()
        #[{a:1, _id:1},{b:2, _id:2}]
        #[1,2]
        result = [v for v in {k: v for d in result for k, v in d.items()}]
        return result
    def add_note(self, note: int) -> None:
        self.__added_notes.insert_one({str(note): note}) 
    
    def liquidate_expired_option(self, code: str) -> None:
        option_date = self._get_third_fryday_next_day(self._month_year_str_to_date(self.position[code]['prazo']))
        inverse_pos = {
          'quantidade': -self.position[code]['quantidade'], 
          'valor_operacao': 0
        }
        temp = self.position
        temp[code] = self.add_negocio(
                                self.position[code],
                                inverse_pos,
                                self._datetime_to_str_date(
                                  option_date
                                ),
                                code
                              )
        data = self._datetime_to_str_date(option_date)
        if data not in temp[code]["trade"]: temp[code]["trade"][data] = []
        temp[code]["trade"][data].append([inverse_pos['quantidade'], inverse_pos['valor_operacao']])
        # temp[code] = self.add_profit_daytrade(temp[code])
        temp = self.add_profit_position(temp, [code], data)
        self.position = temp
    
    def check_expired_options(self) -> None:
        today = datetime.now()
        for key, pos in self.position.items():
          if pos['prazo'] and pos['quantidade']:
            option_date = self._get_third_fryday_next_day(self._month_year_str_to_date(pos['prazo']))
            if option_date < today :
              temp = self.position
              temp[key]['expirado'] = "true"
              self.position = temp
              continue
          temp = self.position
          temp[key]['expirado'] = "false"
          self.position = temp

    def _datetime_to_str_date(self, date: datetime) -> str:
      return date.strftime("%d/%m/%Y")
    
    def _month_year_str_to_date(self, str_date: str, ) -> datetime:
      return datetime.strptime(str_date, "%m/%y")
    
    def _get_third_fryday_next_day(self, date: datetime) -> datetime:
      friday_number = 0
      #Get the previous month last day
      date = date.replace(day = 1) - timedelta(days=1)
      while friday_number < 3:
        date = date + timedelta(days=1)
        if date.weekday() == 4: friday_number += 1
      return date
        
    def atualizar_posicao(self, notas: list) -> None:
    #Atualiza a posição atual com todos os negócios de todas as notas de corretagem processadas
      for i, nota in enumerate(notas):
          data = nota["data"]
          if str(nota["nota"]) not in self.added_notes:
            self.add_note(nota["nota"])
            codigos = []
            for j, negocio in enumerate(nota["negocios"]):
                if negocio["obs"] == 'D': negocio["codigo"] = negocio["codigo"]+"D" 
                if negocio["codigo"] not in codigos: codigos.append(negocio["codigo"])
                if negocio["codigo"] in list(self.position.keys()):
                    k = negocio["codigo"]
                    #ma = preço médio anterior
                    #qa = quantidade anterior
                    #m = preço médio atual (Valor da Operação)
                    #q = quantidade atual
                    # Novo preço médio = ((ma*qa)+m)/(qa+q)
                    negocio["quantidade"] = negocio["quantidade"] if negocio["cv"]=="C" else -negocio["quantidade"]
                    negocio["valor_operacao"] = negocio["valor_operacao"] if negocio["cv"]=="C" else -negocio["valor_operacao"]
                    negocio["valor_operacao"] += nota["custos"]["total"]*negocio['custo_proporcional']
                    position_temp = self.position
                    if data not in position_temp[negocio["codigo"]]["trade"]: position_temp[negocio["codigo"]]["trade"][data] = []
                    position_temp[negocio["codigo"]]["trade"][data].append([negocio["quantidade"], negocio["valor_operacao"]])
                    position_temp[negocio["codigo"]] = self.add_negocio(position_temp[negocio["codigo"]],negocio, data, k)
                    self.position = position_temp
                    
                else:
                    negocio["quantidade"] = negocio["quantidade"] if negocio["cv"]=="C" else -negocio["quantidade"]
                    negocio["valor_operacao"] = negocio["valor_operacao"] if negocio["cv"]=="C" else -negocio["valor_operacao"]
                    valor = negocio["valor_operacao"] + nota["custos"] ["total"]*negocio['custo_proporcional']
                    preco_medio = valor/negocio["quantidade"]
                    position_temp = self.position
                    position_temp[negocio["codigo"]] = {
                        "ativo": negocio["codigo"],
                        "quantidade": negocio["quantidade"],
                        "prazo": negocio["prazo"],
                        "valor": valor,
                        "quantidade_novo": 0,
                        "preco_medio_novo": 0,
                        "preco_medio": preco_medio,
                        "lucro": {},
                        "lucro_daytrade": {},
                        "lucro_normal": {},
                        "trade": {data: [[negocio["quantidade"], valor]]},
                        "expirado": "false",
                    }
                    self.position = position_temp  
            temp = self.position
            temp = self.add_profit_position(temp, codigos, data)
            self.position = temp
            for codigo in codigos:
              if codigo[-1] == "D" and self.position[codigo]["quantidade"] != 0:
                nota_residual = copy.deepcopy(nota)
                nota_residual["nota"] = nota["nota"]*-1
                nota_residual["custos"]["total"] = 0.0
                nota_residual["negocios"] = [
                    {
                      "index": 0,
                      "negociacao": "1-BOVESPA",
                      "cv": "C" if self.position[codigo]["quantidade"] > 0 else "D",
                      "tipo_mercado": "VISTA",
                      "nome_pregao": codigo[:-1], #código sem o D no final
                      "quantidade": abs(self.position[codigo]["quantidade"]), #na nota é sempre positivo
                      "preco": self.position[codigo]["preco_medio"],
                      "valor_operacao": abs(self.position[codigo]["preco_medio"]*self.position[codigo]["quantidade"]), #na nota é sempre positivo
                      "obs": "",
                      "custo_proporcional": 1,
                      "dc": "C",
                      "codigo": codigo[:-1],
                }]
                self.atualizar_posicao([nota_residual])
                temp_position_zerar_codigo = self.position
                temp_position_zerar_codigo[codigo] = {
                    "ativo": codigo,
                    "quantidade": 0,
                    "prazo": self.position[codigo]["prazo"],
                    "valor": 0,
                    "quantidade_novo": 0,
                    "preco_medio_novo": 0,
                    "preco_medio": 0,
                    "lucro": self.position[codigo]["lucro"],
                    "lucro_daytrade": self.position[codigo]["lucro_daytrade"],
                    "lucro_normal": self.position[codigo]["lucro_normal"],
                    "trade": self.position[codigo]["trade"],
                    "expirado": "true"
                }
                self.position = temp_position_zerar_codigo
    
    def add_profit_position (self, temp: dict, codigos: list, data: str) -> dict:
      for codigo in codigos:
        tipo_lucro = "lucro_normal"
        if codigo[-1] == 'D': tipo_lucro = 'lucro_daytrade'
        if data in temp[codigo]["trade"]:
          for trade in temp[codigo]["trade"][data]:
              if trade[0] == 0: continue
              valor_atual = temp[codigo]["preco_medio_novo"]*temp[codigo]["quantidade_novo"]
              temp_qtde = temp[codigo]["quantidade_novo"] + trade[0]
              temp_valor = valor_atual + trade[1]
              temp_medio = temp_valor/temp_qtde if temp_qtde else 0
              if temp[codigo]["quantidade_novo"]:
                if trade[0]/abs(trade[0]) != temp[codigo]["quantidade_novo"]/abs(temp[codigo]["quantidade_novo"]):
                  if data not in temp[codigo][tipo_lucro]: temp[codigo][tipo_lucro][data] = 0 
                  qtde_zerado = trade[0]
                  valor_zerado = trade[1]
                  temp_medio = 0
                  if temp_qtde:
                    temp_medio = temp[codigo]["preco_medio_novo"] 
                    if temp_qtde/abs(temp_qtde) != temp[codigo]["quantidade_novo"]/abs(temp[codigo]["quantidade_novo"]):
                      temp_medio = trade[1]/trade[0]
                      qtde_zerado = -temp[codigo]["quantidade_novo"]
                      valor_zerado = qtde_zerado*temp_medio
                  temp[codigo][tipo_lucro][data] += qtde_zerado*temp[codigo]["preco_medio_novo"] - valor_zerado
              temp[codigo]["quantidade_novo"] = temp_qtde
              temp[codigo]["preco_medio_novo"] = temp_medio
          del temp[codigo]["trade"][data]
      return temp

    #Adiciona um negócio de nota de corretagem à posição atual 
    def add_negocio(self, posicao: dict, negocio: dict, data: str, codigo: str):
      lucro_index = "lucro"
      lucro = posicao[lucro_index]
      if negocio["quantidade"] == 0:
        return posicao
      quantidade_temp = posicao["quantidade"]+negocio["quantidade"]
      #Se ficou negativo, roda uma vez para zerar e a outra para abrir posição contrária
      negocio_valor_inicial = negocio["valor_operacao"] 
      negocio_quantidade_inicial = negocio["quantidade"]
      if quantidade_temp*posicao["quantidade"] < 0:
        quantidade = 0
        negocio["valor_operacao"] = negocio["valor_operacao"] - ( negocio["valor_operacao"]/negocio["quantidade"]*(quantidade_temp-quantidade))
        negocio["quantidade"] = negocio["quantidade"] - quantidade_temp-quantidade
      else:
        quantidade = quantidade_temp
      if abs(quantidade) > abs(posicao["quantidade"]):
        valor = posicao["valor"]+negocio["valor_operacao"]
        preco_medio = valor/quantidade
        lucro = posicao[lucro_index]
      else:
        if data in posicao[lucro_index]:
          lucro[data] = posicao[lucro_index][data] + (negocio["quantidade"]*posicao["preco_medio"]-negocio["valor_operacao"])
        else:
          lucro[data] = (negocio["quantidade"]*posicao["preco_medio"]-negocio["valor_operacao"])
        valor = quantidade* posicao["preco_medio"]
        preco_medio = posicao["preco_medio"] if quantidade != 0 else 0
      if lucro_index == 'lucro':
        posicao_temp = {
            "ativo": posicao['ativo'],
            "quantidade": quantidade,
            "prazo": posicao['prazo'],
            "preco_medio": preco_medio,
            "quantidade_novo": posicao["quantidade_novo"],
            "preco_medio_novo": posicao["preco_medio_novo"],
            "valor": valor,
            "lucro": lucro,
            "lucro_daytrade": posicao["lucro_daytrade"],
            "lucro_normal": posicao["lucro_normal"],
            "trade": posicao['trade'],
            "expirado": "false",
        }
      negocio_temp = {"quantidade": quantidade_temp-quantidade, "valor_operacao": negocio_valor_inicial/negocio_quantidade_inicial*(quantidade_temp-quantidade)}
      return self.add_negocio(posicao_temp, negocio_temp, data, codigo)
