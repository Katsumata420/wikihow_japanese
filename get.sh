
mkdir -p data/html
mkdir -p data/json
mkdir -p data/output

bash crawl_article.sh
bash scrape2jsonl.sh
pythopn script/make_data.py data/json data/output data/divide_data.tsv
