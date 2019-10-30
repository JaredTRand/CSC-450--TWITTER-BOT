from selenium import webdriver
from selenium.webdriver.common.keys import Keys


def follow():
    driver = webdriver.Firefox()
    driver.get('https://twitter.com/explore')
    assert 'Twitter' in driver.title
    driver.find_element_by_id('Explore')


if __name__ == '__main__':
    follow()
