import json
import re

def get_data(json_file):
    with open(json_file,'r') as file:
        attractions_data = json.load(file)
        attractions = attractions_data['result']['results']
        for i,j in enumerate(attractions):
            pattern = r'https:\/\/[^"]+?\.(?:jpg|JPG|png|PNG)'
            matches = re.findall(pattern, j['file'])
            images = [image.replace('\/','/')for image in matches]
            print(f'match\n',matches)



get_data('./data/taipei-attractions.json')