import sys
import json
import re

from bs4 import BeautifulSoup

"""
convert a html file to the json file 
  input: single html file
  output: json file
"""

def reformat_html2dict(bs4_html):
    output_dict = {'meta_title': '', 'original_title': '', 'num_part': -1,
                    'part_name_exist': False, 'contents': [],}
    content_dict = {'part_title': '', 'part_contents': [],}
    part_content_dict = {'bold_line': '', 'article': ''}
 
    # delete only zenkaku space
    preprocess_table = str.maketrans({
      '\u3000': '',
      # ' ': '',
    })

    meta_title = bs4_html.find('title').text
    parts_article_in_page = bs4_html.find_all('ol', {'class': 'steps_list_2'})

    parts_name_in_page = \
        bs4_html.find_all('div', {'class': 'method_toc_item toc_method'})
    parts_name_in_page = [i.text.strip() for i in parts_name_in_page]
    if len(parts_article_in_page) != len(parts_name_in_page):
        parts_name_in_page_hidden = \
            bs4_html.find_all('div', {'class': 'method_toc_item toc_method toc_hidden'})
        parts_name_in_page_hidden = [i.text.strip() for i in parts_name_in_page_hidden]
        parts_name_in_page.extend(parts_name_in_page_hidden)

    if len(parts_article_in_page) == len(parts_name_in_page):
        output_dict['part_name_exist'] = True
    elif len(parts_article_in_page) > len(parts_name_in_page):
        parts_name_in_page = ['' for i in range(len(parts_article_in_page))]
    else:
        raise ValueError()

    # part 内で article または bold_line の対応が取れていない数
    missing_count = 0
    for part_article, part_name in zip(parts_article_in_page, parts_name_in_page): 
        content_dict = {'part_title': '', 'part_contents': [],}

        paragraphs = part_article.find_all('div', {'class': 'step'})
        temp_non_missing_count = 0 # 正しく対応が取れている数
        for paragraph in paragraphs:
            part_content_dict = {'bold_line': '', 'article': ''}

            # delete link, script, image and unicode for paragraph
            while paragraph.find('sup'):
                paragraph.find('sup').decompose()
            while paragraph.find('script'):
                paragraph.find('script').decompose()
            while paragraph.find('a', {'class': 'image'}):
                paragraph.find('a', {'class': 'image'}).decompose()
            while paragraph.find('span', {'class': 'Unicode'}):
                paragraph.find('span', {'class': 'Unicode'}).decompose()

            bold_lines = paragraph.find_all('b', {'class': 'whb'})
            # bold_lines = paragraph.find_all('b') # whb が tgt になる bold

            def can_find_all(bs4_lists):
                # O(n^2)
                flag = True
                for bs4_item_a in bs4_lists:
                    for bs4_item_b in bs4_lists:
                        if bs4_item_a != bs4_item_b and \
                                str(bs4_item_a) in str(bs4_item_b):
                            flag = False        
                            return flag
                return flag

            if can_find_all(bold_lines):
                for bold_line in bold_lines:
                    # delete link, script, image and unicode for bold_line
                    while bold_line.find('sup'):
                        bold_line.find('sup').decompose()
                    while bold_line.find('script'):
                        bold_line.find('script').decompose()
                    while bold_line.find('a', {'class': 'image'}):
                        bold_line.find('a', {'class': 'image'}).decompose()
                    while bold_line.find('span', {'class': 'Unicode'}):
                        bold_line.find('span', {'class': 'Unicode'}).decompose()
                bold_line = ''.join([x.text for x in bold_lines]).strip()
            else:
                # delete link, script, image and unicode for bold_line
                bold_line = paragraph.find('b')
                while bold_line.find('sup'):
                    bold_line.find('sup').decompose()
                while bold_line.find('script'):
                    bold_line.find('script').decompose()
                while bold_line.find('a', {'class': 'image'}):
                    bold_line.find('a', {'class': 'image'}).decompose()
                while bold_line.find('span', {'class': 'Unicode'}):
                    bold_line.find('span', {'class': 'Unicode'}).decompose()
                bold_line = bold_line.text.strip()
        
            article = paragraph.text.strip().replace(bold_line, '')
            bold_line = bold_line.translate(preprocess_table).strip()
            article = article.translate(preprocess_table)
            part_content_dict['bold_line'] = bold_line
            part_content_dict['article'] = article.replace('\n', '')

            content_dict['part_contents'].append(part_content_dict)

            if bold_line != '' and article.replace('\n', '') != '':
                temp_non_missing_count += 1

        if temp_non_missing_count == 0:
            missing_count += 1
        content_dict['part_title'] = part_name
        output_dict['contents'].append(content_dict)

    output_dict['meta_title'] = meta_title
    output_dict['num_part'] = len(parts_name_in_page) - missing_count

    return output_dict
    

def main():
    input_html = sys.argv[1]
    output_json = sys.argv[2]
    parsed_html = BeautifulSoup(open(input_html), 'html.parser')

    output_dict = reformat_html2dict(parsed_html)
    title_name = input_html.split('/')[-1]
    output_dict['original_title'] = title_name

    h = open(output_json, 'w')
    json.dump(output_dict, h, ensure_ascii=False, indent=2, sort_keys=True, separators=(',', ': '))


if __name__ == '__main__':
    main()
