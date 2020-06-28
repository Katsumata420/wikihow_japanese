
html_dir=data/html
for f in $(find $html_dir -mindepth 2 -name "How_to*");
do
    name=`basename $f`
    echo $f
    output=data/json/$name
    python script/scrape4json.py $f $output
done
