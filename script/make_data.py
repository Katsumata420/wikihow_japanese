"""
divide jsonl files into train/dev/test files
  based on a tsv file.
"""

import sys
import os

import make_jsonl

def load_tsv(file_path):
    data = list()
    with open(file_path) as i_f:
        for idx, line in enumerate(i_f):
            if idx == 0:
                continue
            name, size, data_type = line.strip().split()
            data.append((name, data_type))
    
    return data

def save_jsonl(data, file_path):
    with open(file_path, 'w') as o_f:
        for j in data:
            o_f.write(j+'\n')

def main():
    json_dir = sys.argv[1]
    output_dir = sys.argv[2]
    divided_tsv = sys.argv[3]

    divided_tsv = load_tsv(divided_tsv) 

    train_data = list()
    dev_data = list()
    test_data = list()
    for name, data_type in divided_tsv:
        file_path = os.path.join(json_dir, name)
        data = make_jsonl.load_data(file_path)
        output_data = make_jsonl.convert_summary(data)
        output_data = make_jsonl.convert_jsonl(output_data)

        if data_type == 'train':
            train_data.extend(output_data)
        elif data_type == 'dev':
            dev_data.extend(output_data)
        elif data_type == 'test':
            test_data.extend(output_data)
        else:
            raise ValueError()

    save_jsonl(train_data, os.path.join(output_dir, 'train.jsonl'))
    save_jsonl(dev_data, os.path.join(output_dir, 'dev.jsonl'))
    save_jsonl(test_data, os.path.join(output_dir, 'test.jsonl'))

if __name__ == '__main__':
    main()
