"""
load url and save html
"""

import sys
import json
import time
import os

import requests

def load_urls(file_path):
    urls = list()
    with open(file_path) as i_f:
        for line in i_f:
            line = line.strip()
            current_url = json.loads(line)
            urls.append(current_url)
        
    return urls

def main():
    category_dict = sys.argv[1]
    output_dict = sys.argv[2]
    urls = load_urls(category_dict)

    for item in urls:
        file_name = item['name']
        url = item['url']
        current_response  = requests.get(url)

        with open(os.path.join(output_dict, file_name), 'w') as o_f:
            o_f.write(current_response.text)

        time.sleep(3)

if __name__ == '__main__':
    main()
