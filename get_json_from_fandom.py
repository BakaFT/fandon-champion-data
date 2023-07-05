import json
import os
import requests
from bs4 import BeautifulSoup
from slpp import slpp as lua

def get_lua_table_string_from_node(pre_node):
    pre_node_text = pre_node.text
    start_marker = '-- <pre>\n'
    end_marker = '\n-- </pre>'
    start_index = pre_node_text.find(start_marker)
    end_index = pre_node_text.find(end_marker)
    if start_index != -1 and end_index != -1:
        start_index += len(start_marker)
        result = pre_node_text[start_index:end_index].strip()
        result = result.replace('return', '')
        return result
    else:
        print("ERROR")
        return None

def remove_useless_data_from_dict(dict):
    # Do something
    res = dict
    return res


FANDOM_PAGE = "https://leagueoflegends.fandom.com/wiki/Module:ChampionData/data"

# Get the html node
html_doc = requests.get(FANDOM_PAGE).text
soup = BeautifulSoup(html_doc, 'html.parser')
pre_node = soup.find('pre', class_='mw-code')

# Get the lua table string
lua_table_text = get_lua_table_string_from_node(pre_node)

# Convert lua table string to python dict
python_dict = lua.decode(lua_table_text)

# Remove useless data from dict
processed_dict = remove_useless_data_from_dict(python_dict)

# Dump it to json file
GH_WORKSPACE = os.environ['GITHUB_WORKSPACE']
JSON_FILE_PATH = os.path.join(GH_WORKSPACE, 'champion_data.json')
json.dump(processed_dict, open(JSON_FILE_PATH, 'w'), indent=4)
