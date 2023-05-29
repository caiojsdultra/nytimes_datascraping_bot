def get_config_info(config_file):
    import json
    with open(config_file) as json_file:
        config = json.load(json_file)
    return config

def filter_month(month: int):
    from datetime import datetime, timedelta

    current_date = datetime.today().strftime('%m/%d/%Y')

    if month <= 0 or month <= 1:
        formatted_data = datetime.today().strftime('%m/01/%Y')
    elif month <= 2:
        formatted_data = datetime.today() - timedelta(days=(month - 1) * 30)
        formatted_data = formatted_data.strftime('%m/01/%Y')

    else:
        filtered_data = datetime.today() - timedelta(days=month * 30)
        formatted_data = filtered_data.strftime('%m/01/%Y')

    return formatted_data, current_date


def manage_sections(section):
    section_path_dictionary = {
        'Any': '//input[@type="checkbox" and @value="any" and @checked=""]',
        'Briefing': "Briefing|nyt://section/5d9d446d-41aa-501d-a798-e618095f10c7",
        'Business': "Business|nyt://section/0415b2b0-513a-5e78-80da-21ab770cb753",
        'Magazine': "Magazine|nyt://section/a913d1fb-3cdf-556b-9a81-f0b996a1a202",
        'Opinion': "Opinion|nyt://section/d7a71185-aa60-5635-bce0-5fab76c7c297",
        'Real Estate': "Real Estate|nyt://section/8447074a-0b68-5da5-889d-bcc1a0c2a629",
        'Sports': "Sports|nyt://section/4381411b-670f-5459-8277-b181485a19ec",
        'Style': "Style|nyt://section/146e2c45-6586-59ef-bc23-90e88fe2cf0a",
        'T Brand': "T Brand|nyt://section/94ed094f-c033-56a6-a35f-78c26b8527be",
        'Technology': "Technology|nyt://section/4224240f-b1ab-50bd-881f-782d6a3bc527",
        'U.S.': "U.S.|nyt://section/a34d3d6c-c77f-5931-b951-241b4e28681c",
        'World': "World|nyt://section/70e865b6-cc70-5181-84c9-8368b3a5c34b",
        'Podcasts': "Podcasts|nyt://section/11079987-ae8d-5f5f-8c2e-8c66d337d2ba",
        'Movies': "Movies|nyt://section/62b3d471-4ae5-5ac2-836f-cb7ad531c4cb"
    }

    selector = section_path_dictionary[section]

    return selector


def create_robot_output_folder():
    import os
    from datetime import datetime

    exec_hours = datetime.today().strftime('%H-%M')
    folder_name = ''.join(['nytimes_output_', exec_hours])
    folder_path = os.path.join('output', folder_name)

    if not os.path.exists(folder_path):
        os.mkdir(folder_path)
    else:
        print(f'Output folder {folder_path} already exists.')

    return folder_path


def count_search_occurrences(text, title_text, desc_text):

    joined_texts = ' '.join([title_text.lower(), desc_text.lower()])
    total_search_occurrences = joined_texts.count(text.lower())
    return total_search_occurrences


def find_dollar(text_title, text_description):
    import re

    full_text = ' '.join([text_title, text_description])
    found_dollar = False
    pattern = '\$[\d,\.]+|\d+(?:[\d,\.]*\s)?(?:dollars?|USD)'
    occurrences = re.findall(pattern, full_text)

    found_dollar = True if len(occurrences) > 0 else False
    return found_dollar

def description_exists(desc_text, paragraphs: int):
    tokenized_desc = desc_text.split(' ')
    description_exists = True
    if paragraphs == 1 and tokenized_desc[1] in 'By' and 3 <= len(tokenized_desc) <= 6:
        description_exists = False

    return description_exists

def manage_used_repos(path, output_file):
    import pandas as pd
    import shutil
    import os

    if os.path.exists(path):
        print('Deleting existing repo: ', path)
        shutil.rmtree(path)
        print('Creating output repo: ', path)
        os.mkdir(path)
    else:
        print('Creating output repo: ', path)
        os.mkdir(path)

    template_path = ''.join(['template/',output_file])
    output = ''.join([path, '/', output_file])
    shutil.copy(template_path, path)
    excel_session = pd.read_excel(output)

    return excel_session

def write_excel_file(df, output_fullpath):
    import pandas

    df.to_excel(output_fullpath, index=True)

    return
