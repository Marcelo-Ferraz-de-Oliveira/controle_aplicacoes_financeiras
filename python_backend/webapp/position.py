from datetime import datetime, timedelta

class Position:
    def __init__(self) -> None:
        self.__position = {}
        self.__added_notes = []
    @property
    def position(self) -> dict:
        return self.__position
    @position.setter
    def position(self, position: dict) -> None:
        self.__position = position
    
    def liquidate_expired_option(self, code: str) -> None:
        option_date = self._get_third_fryday_next_day(self._month_year_str_to_date(self.position[code]['prazo']))
        inverse_pos = {
          'quantidade': -self.position[code]['quantidade'], 
          'valor_operacao': 0
        }
        self.position[code] = self.add_negocio(
                                self.position[code],
                                inverse_pos,
                                self._datetime_to_str_date(
                                  option_date
                                )
                              )
    
    def check_expired_options(self) -> None:
        today = datetime.now()
        for key, pos in self.position.items():
          if pos['prazo'] and pos['quantidade']:
            option_date = self._get_third_fryday_next_day(self._month_year_str_to_date(pos['prazo']))
            if option_date < today :
              self.position[key]['expirado'] = "true"
              continue
          self.position[key]['expirado'] = "false"
          
    
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
          if nota["nota"] not in self.__added_notes:
            self.__added_notes.append(nota["nota"])
            for j, negocio in enumerate(nota["negocios"]):
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
                    self.position[negocio["codigo"]] = self.add_negocio(self.position[negocio["codigo"]],negocio, data)
                else:
                    negocio["quantidade"] = negocio["quantidade"] if negocio["cv"]=="C" else -negocio["quantidade"]
                    negocio["valor_operacao"] = negocio["valor_operacao"] if negocio["cv"]=="C" else -negocio["valor_operacao"]
                    valor = negocio["valor_operacao"] + nota["custos"]["total"]*negocio['custo_proporcional']
                    preco_medio = valor/negocio["quantidade"]
                    self.position[ negocio["codigo"]] = {
                        "ativo": negocio["codigo"],
                        "quantidade": negocio["quantidade"],
                        "prazo": negocio["prazo"],
                        "valor": valor,
                        "preco_medio": preco_medio,
                        "lucro": {},
                        "expirado": "false",
                    }
    #Adiciona um negócio de nota de corretagem à posição atual
    def add_negocio(self, posicao: dict, negocio: dict, data: str):
      lucro = {}
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
          "valor": valor,
          "lucro": lucro,
          "expirado": "false",
      }
      negocio_temp = {"quantidade": quantidade_temp-quantidade, "valor_operacao": negocio_valor_inicial/negocio_quantidade_inicial*(quantidade_temp-quantidade)}
      return self.add_negocio(posicao_temp, negocio_temp, data)
