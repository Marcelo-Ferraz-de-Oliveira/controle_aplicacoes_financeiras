from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

"""

Module to get B3 prices from symbols (stocks, options, etc).

Receive a list of symbols and yield a dict in that format:
{"symbol": "0.0", "symbol2": "0.0"}

In case of a invalid symbol, the function return a empty string as price
"""

def get_b3_prices(symbols_list, query_interval = 5, load_timeout=30):
  #Open the B3 price consulting page and return a generator (to keep open the page)
  URL_QUERY_B3 = "https://www.b3.com.br/pt_br/market-data-e-indices/servicos-de-dados/market-data/cotacoes/outros-ativos.htm"
  if type(symbols_list) not in (list, tuple, set): raise TypeError("Symbols must be list or tuple or set.")
  wd = get_headless_selenium_webdriver()
  wd.set_page_load_timeout(load_timeout)
  try: 
    wd.get(URL_QUERY_B3)
    while True:
      yield {element:get_price(element,wd) for element in symbols_list} 
      sleep(query_interval)
  finally:
    wd.close()
    
def get_headless_selenium_webdriver():
  options = webdriver.ChromeOptions()
  options.add_argument('--headless')
  options.add_argument('--no-sandbox')
  options.add_argument('--disable-dev-shm-usage')
  return webdriver.Chrome('chromedriver',options=options)

def get_price(symbol, wd, iter_limit = 100):
  #Get symbol price from selenium webdriver opened in B3 price consulting page
  ID_SEARCH_FIELD = "txtCampoPesquisa"
  ID_PRICE = "cotacaoAtivo"
  ID_NAO_ENCONTRADO = "msgNaoEncontrado"
  try:
    field = wd.find_element('id', ID_SEARCH_FIELD)
  except Exception as e:
    print(e)
    return ""
  field.clear()
  field.send_keys(symbol)
  field.send_keys(Keys.ENTER)
  for _ in range(iter_limit):
    not_found = wd.find_element('id', ID_NAO_ENCONTRADO).value_of_css_property("display") == 'block'
    if not_found: return ""
    price = wd.find_element('id', ID_PRICE).text.replace("_","")
    if price: return price
    sleep(0.1)
  return ""

if __name__ == "__main__":
  ativo = ("ABEV3","ABEVC157","PETR4","BBDC4","BBAS3","ITUB4")
  preco =  get_b3_prices(ativo,5)
  for _ in range(5):
    cotacao = next(preco)
    if not cotacao: 
      print("Erro ao obter as cotações")
      break
    print(cotacao)