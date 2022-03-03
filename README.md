# Controle-aplicacoes-financeiras

Aplicação para controlar aplicações financeiras e calcular o imposto de renda a ser pago, através da importação automática das notas de corretagem.

**EM DESENVOLVIMENTO**

### Como instalar:

A aplicação utiliza um backend python/flask com frontend react

Testada apenas no Kubuntu 20.04!

Para instalar e executar a aplicação, juntamente com suas dependências, inicie um ambiente linux com apt (Debian/Ubuntu) e execute:

```
git clone https://github.com/Marcelo-Ferraz-de-Oliveira/controle_aplicacoes_financeiras.git
cd controle-aplicacoes-financeiras
make install
make start
```

Acesse em um navegador no endereço `http://localhost:3000`

Para interromper a execução:

```
make stop
```
