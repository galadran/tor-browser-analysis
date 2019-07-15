from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException,JavascriptException,WebDriverException
from selenium.webdriver.firefox.options import Options,FirefoxBinary,FirefoxProfile
from tqdm import tqdm

torPath = "../tor-browser-patched/Primary/start-tor-browser.desktop"
profilePath = "../tor-browser-patched/Primary/Browser/TorBrowser/Data/Browser/profile.default"
profile = FirefoxProfile(profilePath)
profile.set_preference("webdriver.load.strategy", "unstable")
binary = FirefoxBinary(torPath)
driver = webdriver.Firefox(firefox_binary=binary,firefox_profile=profile)

driver.get('www.google.com')