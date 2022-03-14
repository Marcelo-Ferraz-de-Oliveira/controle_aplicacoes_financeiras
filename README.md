# Controle-aplicacoes-financeiras

Software para ler notas de negociação (corretagem), consolidar a posição acionária e calcular o lucro e imposto de renda a pagar.

Atualmente suporta notas de negociação das corretoras XP, Clear e Genial.

## Como utilizar:

Use uma das formas abaixo para testar a aplicação.

Existem notas de negociação para testes na pasta <a href= "https://github.com/Marcelo-Ferraz-de-Oliveira/controle_aplicacoes_financeiras/tree/main/notas_pdf">notas_pdf</a>

### Live Demo:

https://controleaplicacoesfinanceiras.herokuapp.com/

### Imagem no Docker Hub:

Há uma imagem pronta no Docker Hub. Para utilizá-la em seu computador, execute:

```
docker pull marceloferrazdeoliveira/controle_aplicacoes_financeiras
docker run --rm -p 3000:3000 controle_aplicacoes_financeiras
```

Acesse em um navegador no endereço http://localhost:3000

Caso você não possua o Docker instalado em seu computador, siga o passo-a-passo de instalação do Docker: https://docs.docker.com/get-docker/

### Executar os servidores em modo de desenvolvimento

A aplicação utiliza um backend python/flask com frontend react

Testada apenas no Kubuntu 20.04!

Para instalar e executar os servidores de desenvolvimento e suas dependências, inicie um ambiente linux com apt (Debian/Ubuntu) e execute:

```
git clone https://github.com/Marcelo-Ferraz-de-Oliveira/controle_aplicacoes_financeiras.git
cd controle-aplicacoes-financeiras
make install
make start
```

Para interromper a execução:

```
make stop
```
