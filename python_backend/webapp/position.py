from datetime import datetime, timedelta

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
                                )
                              )
        data = self._datetime_to_str_date(option_date)
        if data not in temp[code]["trade"]: temp[code]["trade"][data] = []
        temp[code]["trade"][data].append([inverse_pos['quantidade'], inverse_pos['valor_operacao']])
        temp[code] = self.add_profit_daytrade(temp[code])
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
                    temp = self.position
                    if data not in temp[negocio["codigo"]]["trade"]: temp[negocio["codigo"]]["trade"][data] = []
                    temp[negocio["codigo"]]["trade"][data].append([negocio["quantidade"], negocio["valor_operacao"]])
                    temp[negocio["codigo"]] = self.add_profit_daytrade(temp[negocio["codigo"]])
                    temp[negocio["codigo"]] = self.add_negocio(temp[negocio["codigo"]],negocio, data)
                    self.position = temp
                else:
                    negocio["quantidade"] = negocio["quantidade"] if negocio["cv"]=="C" else -negocio["quantidade"]
                    negocio["valor_operacao"] = negocio["valor_operacao"] if negocio["cv"]=="C" else -negocio["valor_operacao"]
                    valor = negocio["valor_operacao"] + nota["custos"] ["total"]*negocio['custo_proporcional']
                    preco_medio = valor/negocio["quantidade"]
                    temp = self.position
                    temp[negocio["codigo"]] = {
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
                    self.position = temp
            temp = self.position
            temp = self.add_profit_position(temp, codigos, data)
            self.position = temp  
    
    def add_profit_position (self, temp: dict, codigos: list, data: str) -> dict:
      for codigo in codigos:
        if codigo == "ABEVE147": print(temp[codigo])
        if data in temp[codigo]["trade"]:
          for trade in temp[codigo]["trade"][data]:
              if codigo == "ABEVE147": print(trade)
              if trade[0] == 0: continue
              valor_atual = temp[codigo]["preco_medio_novo"]*temp[codigo]["quantidade_novo"]
              temp_qtde = temp[codigo]["quantidade_novo"] + trade[0]
              temp_valor = valor_atual + trade[1]
              temp_medio = temp_valor/temp_qtde if temp_qtde else 0
              if temp[codigo]["quantidade_novo"]:
                if trade[0]/abs(trade[0]) != temp[codigo]["quantidade_novo"]/abs(temp[codigo]["quantidade_novo"]):
                  if data not in temp[codigo]["lucro_normal"]: temp[codigo]["lucro_normal"][data] = 0 
                  qtde_zerado = trade[0]
                  valor_zerado = trade[1]
                  temp_medio = 0
                  if temp_qtde:
                    temp_medio = temp[codigo]["preco_medio_novo"] 
                    if temp_qtde/abs(temp_qtde) != temp[codigo]["quantidade_novo"]/abs(temp[codigo]["quantidade_novo"]):
                      temp_medio = trade[1]/trade[0]
                      qtde_zerado = -temp[codigo]["quantidade_novo"]
                      valor_zerado = qtde_zerado*temp_medio
                  temp[codigo]["lucro_normal"][data] += qtde_zerado*temp[codigo]["preco_medio_novo"] - valor_zerado
              temp[codigo]["quantidade_novo"] = temp_qtde
              temp[codigo]["preco_medio_novo"] = temp_medio
          del temp[codigo]["trade"][data]
        if codigo == "ABEVE147": print(temp[codigo])
      return temp
    
    def add_profit_daytrade (self, posicao: dict) -> dict:
      for day in posicao["trade"]:
        buy = [0,0]
        sell = [0,0]
        for trade in posicao["trade"][day]:
          if trade[0] > 0:  
            buy[0] += trade[0]
            buy[1] += trade[1]
          else:
            sell[0] += trade[0]
            sell[1] += trade[1]
        posicao["trade"][day] = [buy, sell]
        #Has day trade:
        if buy[0] and sell[0]:
          unitary_profit = (sell[1]/sell[0]) - (buy[1]/buy[0])
          if day not in posicao["lucro_daytrade"]: posicao["lucro_daytrade"][day] = 0
          lucro = 0
          if buy[0] >= sell[0]:
            lucro = -sell[0]*unitary_profit
            buy = [buy[0]+sell[0], (buy[1]/buy[0])*(buy[0]+sell[0])]
            posicao["trade"][day] = [buy, [0,0]]
          if buy[0] < sell[0]:
            lucro = buy[0]*unitary_profit
            sell = [sell[0]+buy[0], (sell[1]/sell[0])*(sell[0]+buy[0])]
            posicao["trade"][day] = [[0,0], sell]
          posicao["lucro_daytrade"][day] += lucro
      return posicao


    #Adiciona um negócio de nota de corretagem à posição atual
    def add_negocio(self, posicao: dict, negocio: dict, data: str):
      lucro = posicao["lucro"]
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
        lucro = posicao["lucro"]
      else:
        if data in posicao["lucro"]:
          lucro[data] = posicao["lucro"][data] + (negocio["quantidade"]*posicao["preco_medio"]-negocio["valor_operacao"])
        else:
          lucro[data] = (negocio["quantidade"]*posicao["preco_medio"]-negocio["valor_operacao"])
        valor = quantidade* posicao["preco_medio"]
        preco_medio = posicao["preco_medio"] if quantidade != 0 else 0
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
      return self.add_negocio(posicao_temp, negocio_temp, data)
