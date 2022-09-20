for d in */ ; 
do 
$(cd "/data/ClickHouse-src/ClickHouse/contrib/$d)")
$("git stash"); 
done