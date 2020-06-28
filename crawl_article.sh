
for f in $(find data/urls -mindepth 1)
do
    echo $f
    bname=`basename $f`
    name=`echo $bname | sed 's/\.[^\.]*$//'`
    mkdir -p data/html/$name
    python script/crawl_article.py $f data/html/$name
done

