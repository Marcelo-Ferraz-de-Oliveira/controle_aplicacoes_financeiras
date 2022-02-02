# Controle-aplicacoes-financeiras

Aplicação para controlar aplicações financeiras através da importação automática das notas de corretagem.

# Pré requisitos

- Python 3.9
- Bibliotecas pandas e tabula-py e flask
- Java runtime (para o tabula-py)

#Modo de uso

##Servidor Backend - Linux
Instale as dependências, clone o repositório e inicie o servidor flask (configurado para teste, no momento).

<code>git clone https://github.com/Marcelo-Ferraz-de-Oliveira/Controle-aplicacoes-financeiras.git
flask run</code>

Passe a nota de corretagem e a senha do PDF como argumento, conforme o exemplo abaixo:
<code>#http://127.0.0.1:5000/negocios?arquivo=nota.pdf&senha=abc</code>
