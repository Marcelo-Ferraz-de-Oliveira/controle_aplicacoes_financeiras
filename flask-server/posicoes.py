

#Adiciona um negócio de nota de corretagem à posição atual
def add_negocio(posicao, negocio):
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
    lucro_total = posicao["lucro_total"]
  else:
    lucro = posicao["lucro"] + (negocio["quantidade"]*posicao["preco_medio"]-negocio["valor_operacao"])
    valor = quantidade* posicao["preco_medio"]
    preco_medio = posicao["preco_medio"] if quantidade != 0 else 0
    if quantidade != 0:
      lucro_total = posicao['lucro_total']
    else:
      lucro_total = posicao['lucro_total'] + lucro
      lucro = 0
  posicao_temp = {
      "ativo": posicao['ativo'],
      "quantidade": quantidade,
      "preco_medio": preco_medio,
      "valor": valor,
      "lucro": lucro,
      "lucro_total": lucro_total
  }
  negocio_temp = {"quantidade": quantidade_temp-quantidade, "valor_operacao": negocio_valor_inicial/negocio_quantidade_inicial*(quantidade_temp-quantidade)}
  return add_negocio(posicao_temp, negocio_temp )



def atualizar_posicao(posicao, notas):
#Atualiza a posição atual com todos os negócios de todas as notas de corretagem processadas
    for i, nota in enumerate(notas):
        for j, negocio in enumerate(nota["negocios"]):
            if negocio["codigo"] in list(posicao.keys()):
                k = negocio["codigo"]
                #ma = preço médio anterior
                #qa = quantidade anterior
                #m = preço médio atual (Valor da Operação)
                #q = quantidade atual
                # Novo preço médio = ((ma*qa)+m)/(qa+q)
                negocio["quantidade"] = negocio["quantidade"] if negocio["cv"]=="C" else -negocio["quantidade"]
                negocio["valor_operacao"] = negocio["valor_operacao"] if negocio["cv"]=="C" else -negocio["valor_operacao"]
                negocio["valor_operacao"] += nota["custos"]["total"]*negocio['custo_proporcional']
                posicao[negocio["codigo"]] = add_negocio(posicao[negocio["codigo"]],negocio)
            else:
                negocio["quantidade"] = negocio["quantidade"] if negocio["cv"]=="C" else -negocio["quantidade"]
                negocio["valor_operacao"] = negocio["valor_operacao"] if negocio["cv"]=="C" else -negocio["valor_operacao"]
                valor = negocio["valor_operacao"] + nota["custos"]["total"]*negocio['custo_proporcional']
                preco_medio = valor/negocio["quantidade"]
                posicao[ negocio["codigo"]] = {
                    "ativo": negocio["codigo"],
                    "quantidade": negocio["quantidade"],
                    "valor": valor,
                    "preco_medio": preco_medio,
                    "lucro": 0,
                    "lucro_total": 0
                }
        
    return posicao
