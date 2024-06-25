import os
import time
import pandas as pd
from ny_utils import utils
from RPA.Browser.Selenium import Selenium
import RPA.HTTP


http = RPA.HTTP.HTTP()
browser = Selenium(auto_close=False, timeout=30,page_load_timeout=30)
configs = utils.get_config_info('config/config.json')

class nytimes_news_management:
    def __init__(self, website, search_text, search_date_range, sections, df):
        self.driver = browser
        self.website = website
        self.search_text = search_text
        self.search_date_range = search_date_range
        self.sections = sections
        self.df = df
    def search_news(self):
        print(f'Searching for news at {self.website}')
        browser.open_available_browser(url=configs['website'], maximized=True)
        browser.click_element_when_visible(locator='//button[@data-testid="Accept all-btn"]')
        browser.click_element_when_visible(locator='//button[@data-testid="search-button"]')
        browser.input_text(text=self.search_text, locator='//input[@data-testid="search-input" and @type="text"]')
        browser.click_element(locator='//button[@data-testid="search-submit" and @type = "submit"]')
        return

    #                                Apply date Filters

    def apply_date_filters(self):
        browser.click_element_if_visible(locator='//button[@data-testid="GDPR-accept"]')

        # Business Rule - number of months for which you need to receive news
        filtered_date, current_date = utils.filter_month(self.search_date_range)

        browser.click_element(locator='//button[@data-testid="search-date-dropdown-a"]')
        browser.click_element(locator='//button[@value="Specific Dates"]')


        browser.input_text(locator='//input[@data-testid="DateRange-startDate" and @id="startDate"]', text=filtered_date)
        browser.input_text(locator='//input[@data-testid="DateRange-endDate" and @id="endDate"]', text=current_date)

        browser.click_element(locator='//button[@data-testid="search-date-dropdown-a"]')
        time.sleep(1)
        return
    #                                Apply Section Filters
    def apply_section_filters(self):

        if self.sections[0] == "":
            return 'No section were selected.'

        browser.click_element_if_visible(locator='xpath=//button[@data-testid="search-multiselect-button"]')

        # Business Rule- your automation should have the option to choose from none to any number of categories/sections

        for section in self.sections:
            locator = utils.manage_sections(section)
            pattern = '//label[@class="css-1a8ayg6" and @data-testid="DropdownLabel"]/input[@type="checkbox" and @data-testid="DropdownLabelCheckbox" and @value="locator"]'
            try:
                browser.click_element(locator=pattern.replace('locator', locator))
                time.sleep(1)
            except Exception as e:
                print(f'Section named {section} was not found')

        browser.click_element_if_visible(locator='xpath=//button[@data-testid="search-multiselect-button"]')
        return
    #                                Manage Search Results
    def manage_search_results(self):
        time.sleep(3)
        search_results = browser.get_text(locator='//p[@class="css-nayoou" and @aria-live="polite" and @aria-atomic="true" and @data-testid="SearchForm-status"]')
        split_search_results = search_results.split()
        search_count = split_search_results[1]
        return search_count

    def finish_process(self):
        browser.close_browser()
        return

    def click_more_button(self):
        show_more_exits = True
        current_height = browser.execute_javascript("return document.body.scrollHeight")
        while show_more_exits:
            time.sleep(1)
            browser.execute_javascript(f"window.scrollTo(0, {current_height});")
            try:
                browser.click_element(locator='//button[@data-testid="search-show-more-button" and @type="button"]')
            except:
                break
            #status = browser.element_should_be_visible(locator='//button[@data-testid="search-show-more-button" and @type="button"]')
            #browser.execute_javascript("window.scrollTo(0, document.body.scrollHeight);")
    def get_news_information(self):

        df = self.df
        counter = 0
        counter_advertisements = 0
        news_count_controller = 0
        news_list = browser.get_webelements(locator='css=ol li')

        for li in news_list:
            counter+=1
            #                           GET TITLE
            text_title=''
            list_information = []

            try:
                text_title = browser.get_element_attribute(locator=f'xpath=/html/body/div/div[2]/main/div[1]/div[2]/*/ol/li[{counter}]/div/div/div/a/h4', attribute='innerHTML')
            except Exception as e:
                #handling advertisements
                print(f'List Item number {counter} is an advertisement')
                counter_advertisements+=1
                continue
            print(f'Title: {text_title}')

            #                            GET DESCRIPTION
            elements = browser.get_webelements(locator=f'css=#site-content > div.css-1wa7u5r > div:nth-child(2) > div.css-46b038 > ol > li:nth-child({counter}) > div > div > div > a > p')
            count_paragraphs = len(elements)
            desc_text = ''
            try:
                desc_text = browser.get_element_attribute(locator=f'css=#site-content > div.css-1wa7u5r > div:nth-child(2) > div.css-46b038 > ol > li:nth-child({counter}) > div > div > div > a > p.css-16nhkrn', attribute='innerHTML')
            except Exception as e:
                desc_text = "<unknown>"
                pass

            #   Handling descriptions not found
            if desc_text != "<unknown>":
                desc_exists = utils.description_exists(desc_text=desc_text, paragraphs=count_paragraphs)
                if desc_exists==False:
                    desc_text='<unknown>'

            print(f'Description: {desc_text}')

            #                            GET DATE

            news_date = ''
            try:
                news_date = browser.get_element_attribute(locator=f'css=#site-content > div.css-1wa7u5r > div:nth-child(2) > div.css-46b038 > ol > li:nth-child({counter}) > div > span', attribute='innerHTML')
            except:
                pass

            print(f'Date: {news_date}')

            #                            GET IMAGE

            image_source=''
            file_name=''
            file_name = ''.join(['news_image_', str(counter),'.jpeg'])
            file_path = ''.join(['output/', file_name])

            try:
                image_source = browser.get_element_attribute(locator=f'css=#site-content > div > div:nth-child(2) > div.css-8xl60i > ol > li:nth-child({counter}) > div > div > figure > div > img',
                                                             attribute='src')

                http.download(url=image_source, target_file=file_path)
            except:
                image_source = '<unknown>'
            #                            COUNT SEARCH PHRASE OCCURRENCES

            count_search_occurrences = utils.count_search_occurrences(text=self.search_text, title_text=text_title, desc_text=desc_text)

            #                            FOUND MONEY CITATIONS
            found_dollar = utils.find_dollar(text_title=text_title, text_description=desc_text)

            #                            STORE INTO DATAFRAME

            list_information.append([text_title, news_date, desc_text, count_search_occurrences, found_dollar, file_name])
            data = pd.DataFrame({
                'TITLE': [list_information[0][0]],
                'DATE': [list_information[0][1]],
                'DESCRIPTION': [list_information[0][2]],
                'SEARCH COUNT': [list_information[0][3]],
                'CONTAINS MONEY': [list_information[0][4]],
                'NEWS PICTURE': [list_information[0][5]]
            })
            df = pd.concat([df, data], ignore_index=True)
            news_count_controller +=1
        return df




