"""
convert json file into summary json
  summary json: including src and tgt key
"""

import json
import sys

def load_data(file_path):
    with open(file_path) as i_f:
        data = json.load(i_f)
    return data

def convert_summary(data):
    output_data = list()
    num_part = data['num_part']
    title = data['original_title']
    contents = data['contents'] # list
    for idx, content in enumerate(contents):
        temp_dict = {'src': '', 'tgt': '', 'title': title+'_{}'.format(idx)}
        part_contents = content['part_contents'] # summary

        src_list = list()
        tgt_list = list()
        for c in part_contents:
            # bold line が空の場合、対応する記事も空にする
            # 逆も然り
            article = c['article']
            bold_line = c['bold_line']
            if article != '' and bold_line != '':
                src_list.append(article)
                tgt_list.append(bold_line)
        
        # 一つも入っていなかったらそもそもデータにならない
        if not src_list:
            continue
        src = ''.join(src_list)
        tgt_list = [t if t[-1] == '。' else t + '。' for t in tgt_list]
        tgt = ''.join(tgt_list)
        # tgt = '。'.join(tgt_list) + '。'

        temp_dict['src'] = src
        temp_dict['tgt'] = tgt

        output_data.append(temp_dict)
    
    return output_data

def convert_jsonl(output_data):
    output_strings = list()
    for part_dict in output_data:
        output_json = json.dumps(part_dict, ensure_ascii=False)
        output_strings.append(output_json)
    return output_strings
    

def main():
    input_json = sys.argv[1]
    input_json = load_data(input_json)

    output_data = convert_summary(input_json) 
    for i in convert_jsonl(output_data):
        print(i)

if __name__ == '__main__':
    main()
