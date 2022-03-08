import pytest
from webapp.headless_webdriver import get_headless_selenium_webdriver
URL_JSONTEST = "http://echo.jsontest.com/key/value/one/two"
EXPECTED_RESULT = '<html><head></head><body><pre style="word-wrap: break-word; white-space: pre-wrap;">{\n   "one": "two",\n   "key": "value"\n}\n</pre></body></html>'
WRONG_URL = "httq://wrongurlexample.inexistent"

def test_get_headless_selenium_webdriver():
    driver = get_headless_selenium_webdriver()
    try:
        driver.get(URL_JSONTEST)
        assert EXPECTED_RESULT == driver.page_source
    finally:
        driver.close()
    with pytest.raises(Exception):
        driver.get(WRONG_URL)
        driver.close()