# Controle-aplicacoes-financeiras

Aplicação para controlar aplicações financeiras através da importação automática das notas de corretagem.

No momento suporta notas fiscais das corretoras:

- XP
- Clear
- Genial

#Modo de uso

## Pré requisitos:

- Python 3.9;
- Bibliotecas python: pandas, tabula-py e flask;
- Java runtime (para o tabula-py);

##Servidor Backend

Clone o repositório e inicie o servidor do flask.

<code>git clone https://github.com/Marcelo-Ferraz-de-Oliveira/Controle-aplicacoes-financeiras.git</code>

<code>mv .flaskenv.example .flaskenv</code>

<code>flask run</code>

Passe a nota de corretagem e a senha do PDF como argumento, conforme o exemplo abaixo:

<code>#http://127.0.0.1:5000/negocios?arquivo=nota.pdf&senha=abc</code>

O servidor retornará os dados da nota em formato JSON.

#Tecnologias utilizadas:

Python flask

react

react-bootstrap

styled-components.com
