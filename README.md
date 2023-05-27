The main steps:

1. Open the site by following the link
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
