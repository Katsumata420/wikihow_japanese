# wikiHow dataset (Japanese version)
- This dataset is based on [a paper](https://arxiv.org/abs/1810.09305), which describes wikiHow English summarization dataset.
- This dataset is crawled from [Japanese wikiHow](https://www.wikihow.jp/%E3%83%A1%E3%82%A4%E3%83%B3%E3%83%9A%E3%83%BC%E3%82%B8) for Japanese summarization dataset.

## Requirements
- Python3
- `pip install -r requirements.txt`

## How to get the dataset
- For quick start, run the script `bash get.sh`.
    - The train/dev/test json files are made in `data/output`.
- In detail, you run the following steps.
1. `bash crawl_article.sh`
    - Crawling each article from the url addresses in `data/urls`.
2. `bash scrape2jsonl.sh`
    - Extract knowledge from the html files crawled in step 1.
        - the extracted info is described in below #json_description.
3. `python script/make_data.py`
    - Make train/dev/test data from the json files extracted in step 2 based on `data/divide_data.tsv`.
        - The detail of the json files is below section.

### json description
- Howtojson

| key | value |
| :---|:--- |
| meta_title | html meta title text |
| num_part | the total part number in the article |
| original_title | title text |
| part_name_exist | exist the part title or not |
| contents | list of part (number is the same as num_part)|
|  - part_title | part title |
|  - part_contents | list of the each step content in the part|
| -- article | the article text in the step |
| -- bold_line | the bold line in the step |



- train/dev/test.json

| key | value |
| :---|:--- |
| src | source text |
| tgt | target text; bold lines in the article |
| title | article title + current part number |

## Related repository
- English wikiHow summarization dataset: https://github.com/mahnazkoupaee/WikiHow-Dataset

## License
The articles are provided by wikiHow.
Content on wikiHow can be shared under a Creative Commons License (CC-BY-NC-SA).
