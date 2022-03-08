from time import sleep
from webapp.headless_webdriver import get_headless_selenium_webdriver, Keys

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
  return "timeout"

