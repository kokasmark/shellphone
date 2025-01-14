import re
import json

def parse_txt_to_dict(txt):
    pattern = r'public\s+const\s+int\s+(\w+)\s*=\s*(\d+);'
    matches = re.findall(pattern, txt)
    result = {name: int(id_) for name, id_ in matches}
    return result

def parse_txt_to_dict_reverse(txt):
    pattern = r'public\s+const\s+int\s+(\w+)\s*=\s*(\d+);'
    matches = re.findall(pattern, txt)
    result = {int(id_): name for name, id_ in matches}
    return result

def convert_txt_to_json(txt_file, json_file,reversed=False):
    with open(txt_file, 'r') as f:
        txt_data = f.read()
    if not reversed:
        data = parse_txt_to_dict(txt_data)
        
        with open(json_file, 'w') as f:
            json.dump(data, f, indent=4)
    if reversed:
        data = parse_txt_to_dict_reverse(txt_data)
        
        with open(json_file, 'w') as f:
            json.dump(data, f, indent=4)

txt_file = 'input.txt'
json_file = 'output.json'

convert_txt_to_json(txt_file, json_file,True)