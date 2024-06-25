import ny_utils.utils
from ny_times_steps import nytimes_news_management
from ny_utils import utils
from RPA.Robocorp.WorkItems import WorkItems

# Comment these variables bellow if running the project locally.
# wi = WorkItems()
# wi.get_input_work_item()

# search_new = wi.get_work_item_variable("SEARCH") #Load the input variable SEARCH_TEXT from this config if running locally.
# date_range = wi.get_work_item_variable("DATE RANGE") #Load the input variable DATE_RANGE from this config if running locally.
# sections = wi.get_work_item_variable("SECTIONS") #Load the input variable SECTIONS from this config if running locally.

configs = utils.get_config_info('config/config.json') #Load the input variables SEARCH_TEXT, DATE_RANGE and SECTIONS from this config if running locally.

search_new = configs["SEARCH"] #Load the input variable SEARCH_TEXT from this config if running locally.
date_range = configs["DATE_RANGE"] #Load the input variable DATE_RANGE from this config if running locally.
sections = configs["SECTIONS"] #Load the input variable SECTIONS from this config if running locally.

return_dataframe = utils.manage_used_repos(configs['output_folder'], configs['output_file_name'])
steps = nytimes_news_management(configs['website'], search_new, date_range, sections,return_dataframe)
output_fullpath = ''.join([configs['output_folder'],'/',configs['output_file_name']])

print('DATAFRAME:', return_dataframe)
print(f'PARAMS: {search_new}, {date_range}, {sections}')

try:
    #                                Search News
    steps.search_news()
    print(f'STEP 1 - Search News')

    #                                Apply date Filters
    # steps.apply_date_filters()
    # print('STEPS 2 - Apply Date Filters')


    #                                Manage Search Results
    steps.apply_section_filters()
    print('STEPS 3 - Apply Section Filters')

    #                                Apply Section Filters
    search_count = steps.manage_search_results()
    print('STEPS 3 - Apply Section Filters')


    #                                Workflow management

    if search_count == '0':
        steps.finish_process()
        print(f"Process is finishing cause no search {configs['search']} results were found")
    else:

        #                               Getting news information
        steps.click_more_button()
        new_df = steps.get_news_information()

        #                               Write Excel File
        utils.write_excel_file(new_df, output_fullpath)
        print('Using this DF to create excel file:', new_df)
        steps.finish_process()
except Exception as e:
    print(f'An error occurred while executing the process: {e}')


