#!/bin/bash

for dir in ./level_*/; do
    # reset level corpus
    > $dir/corpus.corpus
    for file in $dir/*.txt; do
        echo "Processing $file"
        cat $file >> $dir/corpus.corpus
    done
done

pushd .
cd level_1/
shuf -r corpus.txt | head -n 120 > corpus.corpus
popd

pushd .
cd level_2/
shuf -r corpus.txt | head -n 500 > corpus.corpus
popd

pushd .
cd level_3/
shuf ../level_2/corpus.txt > corpus.1.corpus
shuf ../level_2/corpus.txt >> corpus.1.corpus
shuf ../level_2/corpus.txt >> corpus.1.corpus
shuf corpus.txt >> corpus.1.corpus
./auto_corpus.sh >> corpus.1.corpus
shuf corpus.1.corpus > corpus.corpus
shuf corpus.1.corpus >> corpus.corpus
shuf corpus.1.corpus >> corpus.corpus

du -h corpus.corpus
popd

pushd .
cd level_4/
# Start with previous levels
cat ../level_3/corpus.corpus > corpus.corpus
# Add all generated level_4 .corpus files with stop tokens
for f in $(find corpus/ -name '*.corpus' -type f | sort); do
    cat "$f" >> corpus.corpus
    echo '<stop>' >> corpus.corpus
done
du -h corpus.corpus
popd
