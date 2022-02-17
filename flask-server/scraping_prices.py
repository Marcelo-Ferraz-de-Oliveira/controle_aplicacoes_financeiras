from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

"""

Module to get B3 prices from symbols (stocks, options, etc).

Receive a list of symbols and yield a dict in that format:
{"symbol": "0.0", "symbol2": "0.0"}

In case of a invalid symbol, the function return a empty string as price
"""


def get_price(symbol, wd, iter_limit = 100):
  #Get symbol price from selenium webdriver opened in B3 price consulting page
  id_search_field = "txtCampoPesquisa"
  id_price = "cotacaoAtivo"
  id_nao_encontrado = "msgNaoEncontrado"
  try:
    field = wd.find_element('id', id_search_field)
  except AttributeError as e:
    raise AttributeError(e)
  except BaseException as e:
    print(e)
    return ""
  field.clear()
  field.send_keys(symbol)
  field.send_keys(Keys.ENTER)
  for _ in range(iter_limit):
    not_found = wd.find_element('id', id_nao_encontrado).value_of_css_property("display") == 'block'
    if not_found: return ""
    price = wd.find_element('id', id_price).text.replace("_","")
    if price: return price
    sleep(0.1)
  return ""

def get_b3_prices(symbols, query_interval = 30):
  #Open the B3 price consulting page and return a generator (to keep open the page)
  if type(symbols) is not list and type(symbols) is not tuple:
    raise TypeError("Symbols must be list or tuple.")
  options = webdriver.ChromeOptions()
  options.add_argument('--headless')
  options.add_argument('--no-sandbox')
  options.add_argument('--disable-dev-shm-usage')
  url_query_b3 = "https://www.b3.com.br/pt_br/market-data-e-indices/servicos-de-dados/market-data/cotacoes/outros-ativos.htm"
  wd = webdriver.Chrome('chromedriver',options=options)
  wd.set_page_load_timeout(30)
  try:
    wd.get(url_query_b3)
  except :
    wd.close()
    yield None
  while True:
    prices = {}
    for symbol in symbols:
      prices.update({symbol:get_price(symbol,wd)})
    yield prices
    sleep(query_interval)

if __name__ == "__main__":
  ativo = ("ABEV3","ABEVC157","PETR4","BBDC4","BBAS3","ITUB4")
  preco =  get_b3_prices(ativo,5)
  for _ in range(5):
    cotacao = next(preco)
    if not cotacao: 
      print("Erro ao obter as cotações")
      break
    print(cotacao)