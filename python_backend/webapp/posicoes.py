
def atualizar_posicao(posicao, notas):
#Atualiza a posição atual com todos os negócios de todas as notas de corretagem processadas
  for i, nota in enumerate(notas):
      data = nota["data"]
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
              posicao[negocio["codigo"]] = add_negocio(posicao[negocio["codigo"]],negocio, data)
          else:
              negocio["quantidade"] = negocio["quantidade"] if negocio["cv"]=="C" else -negocio["quantidade"]
              negocio["valor_operacao"] = negocio["valor_operacao"] if negocio["cv"]=="C" else -negocio["valor_operacao"]
              valor = negocio["valor_operacao"] + nota["custos"]["total"]*negocio['custo_proporcional']
              preco_medio = valor/negocio["quantidade"]
              posicao[ negocio["codigo"]] = {
                  "ativo": negocio["codigo"],
                  "quantidade": negocio["quantidade"],
                  "prazo": negocio["prazo"],
                  "valor": valor,
                  "preco_medio": preco_medio,
                  "lucro": {},
              }
      
  return posicao


#Adiciona um negócio de nota de corretagem à posição atual
def add_negocio(posicao, negocio, data):
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
      "lucro": lucro
  }
  negocio_temp = {"quantidade": quantidade_temp-quantidade, "valor_operacao": negocio_valor_inicial/negocio_quantidade_inicial*(quantidade_temp-quantidade)}
  return add_negocio(posicao_temp, negocio_temp, data)

def assembly_posicao(ativo,quantidade,prazo,valor,preco_medio,lucro,lucro_total):
  if type(lucro) == type(lucro_total) == dict:
    return {
            "ativo": ativo,
            "quantidade": quantidade,
            "prazo": prazo,
            "valor": valor,
            "preco_medio": preco_medio,
            "lucro": lucro
          }
  else: raise ValueError("Lucro não é um dicionário no formato {data1:lucro1,data2:lucro2}")

def zerar_opcoes_expiradas(posicao):
  pass