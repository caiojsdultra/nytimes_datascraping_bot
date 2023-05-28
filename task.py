import ny_utils.utils
from ny_times_steps import nytimes_news_management
from ny_utils import utils

from RPA.Robocorp.WorkItems import WorkItems

wi = WorkItems()
wi.get_input_work_item()
search_new = wi.get_work_item_variable("SEARCH")
date_range = wi.get_work_item_variable("DATE RANGE")
sections = wi.get_work_item_variable("SECTIONS")

configs = utils.get_config_info('config/config.json')

return_dataframe = utils.get_output_dataframe(configs['output_folder'], configs['output_file_name'])
steps = nytimes_news_management(configs['website'], search_new, date_range, sections,return_dataframe)
output_fullpath = ''.join([configs['output_folder'],'/',configs['output_file_name']])

print('DATAFRAME:', return_dataframe)
print(f'PARAMS: {search_new}, {date_range}, {sections}')

try:
    #                                Search News
    steps.search_news()
    print(f'STEP 1 - Search News')

    #                                Apply date Filters
    steps.apply_date_filters()
    print('STEPS 2 - Apply Date Filters')


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

    if len(new_df) > 0:
        utils.write_excel_file(new_df, output_fullpath)

    print(f'An error occurred while executing the process: {e}')


