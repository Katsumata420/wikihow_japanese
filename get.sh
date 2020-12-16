
mkdir -p data/html
mkdir -p data/json
mkdir -p data/output

bash crawl_article.sh
bash scrape2jsonl.sh
python script/make_data.py data/json data/output data/divided_data.tsv
