NOTE - The bot on Robocorp Cloud receives the following parameters through json file:
SEARCH - Should be a String,
DATE_RANGE - Should be an int (as said on challenge's description),
SECTIONS - Should be a list of strings (ex: (["Opinion", "Business"])

## -> The Challenge

Your challenge is to automate the process of extracting data from the news site. Link to the news site: [www.nytimes.com](http://www.nytimes.com/)

You must have 3 configured variables (you can save them in the configuration file, but it is better to put them to the Robocorp Cloud [Work Items](https://robocorp.com/docs/libraries/rpa-framework/rpa-robocorp-workitems/keywords#get-work-item-variable)):

- search phrase
- news category or section
- number of months for which you need to receive news
    
    > Example of how this should work: 0 or 1 - only the current month, 2 - current and previous month, 3 - current and two previous months, and so on

The main steps:

1. Open the website by following the link
2. Enter a phrase in the search field
3. On the result page, apply the following filters:
    - select a news category or section
        
        > your automation should have the option to choose from none to any number of categories/sections. This should be specified via the config file or/and Robocorp Cloud Work Items
        > 
    - choose the latest (i.e., newest) news
4. Get the values: title, date, and description.
5. Store in an Excel file:
    - title
    - date
    - description (if available)
    - picture filename
    - count of search phrases in the title and description
    - True or False, depending on whether the title or description contains any amount of money
        
        > Possible formats: $11.1 | $111,111.11 | 11 dollars | 11 USD
        > 
6. Download the news picture and specify the file name in the Excel file
7. Follow steps 4-6 for all news that falls within the required time period
