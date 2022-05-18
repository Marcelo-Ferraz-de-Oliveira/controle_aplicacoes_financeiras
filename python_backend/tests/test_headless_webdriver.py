import pytest
from webapp.headless_webdriver import get_headless_selenium_webdriver
URL_JSONTEST = "http://echo.jsontest.com/key/value/one/two"
EXPECTED_RESULT = '{\n   "one": "two",\n   "key": "value"\n}'
WRONG_URL = "httq://wrongurlexample.inexistent"

def test_get_headless_selenium_webdriver():
    driver = get_headless_selenium_webdriver()
    try:
        driver.get(URL_JSONTEST)
        result = driver.find_element_by_tag_name("pre").text
        assert EXPECTED_RESULT == result
    finally:
        driver.close()
    with pytest.raises(Exception):
        driver.get(WRONG_URL)
        driver.close()