from RPA.Browser.Selenium import Selenium
import RPA.HTTP


http = RPA.HTTP.HTTP()
browser = Selenium(auto_close=False, timeout=30,page_load_timeout=30)
counter = 1

browser.open_available_browser("https://nytimes.com", maximized=True)

browser.click_element_when_visible(locator='//button[@data-testid="Accept all-btn"]')
browser.click_element_when_visible(locator='//button[@data-testid="search-button"]')
browser.input_text(text="Ja Morant", locator='//input[@data-testid="search-input" and @type="text"]')
browser.click_element(locator='//button[@data-testid="search-submit" and @type = "submit"]')

image_source = browser.get_element_attribute(
    locator=f'css=#site-content > div > div:nth-child(2) > div.css-8xl60i > ol > li:nth-child({counter}) > div > div > figure > div > img',
        attribute='src'
    )

print(image_source)