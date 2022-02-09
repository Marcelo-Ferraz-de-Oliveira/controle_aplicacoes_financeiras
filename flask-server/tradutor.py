
#Tradutor de Nome do Pregão B3 para Código de Negociação
#suporte a todos os instrumentos da B3
from builtins import ValueError
import json
import re
import pandas as pd




#print(codigos_b3)

#Função para construir string da expressão regular
#A expressão buscará pela presença de qualquer um dos sufixos do Nome do Pregão
# no formato: r'(ON|PN|CI).*$' (Quaquer um dos sufixos+quaisquer caracteres após o sufixo até o fim da string)
def construir_string(codigos_b3_tipos):   
    string = r'('
    #Ordena pelo tamanho (len) da chave.
    #Assim, será analisado primeiro o sufixo maior (PNA antes de PN por exemplo)
    for nome in sorted(codigos_b3_tipos, key=len, reverse=True):
        nome = nome.replace("*","\*")
        string = string+str(nome)+r'|'
    #Retira o último caracter | e termina a montagem
    string = string[:-1] + r').*$'
    return string

#Encontra o sufixo no Nome do Pregão, e retorna seu código
def sufixo_para_numero(nome_pregao, r_string, codigos_b3_tipos):
    try:
        nome_pregao = re.findall(r_string,nome_pregao)[0]
    except:
        raise ValueError("Sufixo não encontrado")
    
    return codigos_b3_tipos[nome_pregao]

#Transforma o Nome do Pregão em Código de Negociação completo (prefixo+sufixo)
def find_code(nome_pregao, r_string, codigos_b3, codigos_b3_tipos):
    try:
        #Tenta encontrar o prefixo na tabela de códigos
        novo_codigo = codigos_b3[re.sub(r_string,'',nome_pregao)] 
    except:
        #Se o prefixo não está na tabela o próximo nome é o prefixo (Derivativos)
        return re.sub(r_string,'',nome_pregao)
        
    return "".join(
            (
                novo_codigo, 
                sufixo_para_numero(nome_pregao, r_string, codigos_b3_tipos)
                )
            )
#Função principal
def nome_pregao_to_codigo(string):
    #Carrega os JSONs com os códigos de negociação
    with open('codigos_b3.json','r') as f:
        codigos_b3 = json.load(f)['Codigo']
    with open('codigos_b3_tipos.json','r') as f:
        codigos_b3_tipos = json.load(f)['TckrSymb']
    #Cria a string de busca de sufixo
    r_string = construir_string(codigos_b3_tipos)
    string = string.replace(" ", "")
    return find_code(string, r_string, codigos_b3, codigos_b3_tipos)

if __name__ == "__main__":
    string = ('ABEVB161ON 15,62', 'AMBEV S/AON', 'IRBRB330ON 3,30','ISHARE SP500CI','PETROBRASPN', 'USIMINASPNA')
    r_esperado = ['ABEVB161','ABEV3','IRBRB330','IVVB11','PETR4','USIM5']
    resultado = []
    for s in string:
        resultado.append(nome_pregao_to_codigo(s))
    #print(resultado)
    print("Teste passou? R: "+ str(resultado == r_esperado))
    
    