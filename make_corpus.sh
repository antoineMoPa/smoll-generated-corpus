#!/bin/bash

shopt -s nullglob

for dir in ./level_*/; do
    # reset level corpus
    > $dir/corpus.corpus
    for file in "${dir}"*.txt; do
        echo "Processing $file"
        cat "$file" >> $dir/corpus.corpus
        echo '<stop>' >> $dir/corpus.corpus
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
shuf ../level_2/corpus.txt | awk '{print; print "<stop>"}' > corpus.1.corpus
shuf ../level_2/corpus.txt | awk '{print; print "<stop>"}' >> corpus.1.corpus
shuf ../level_2/corpus.txt | awk '{print; print "<stop>"}' >> corpus.1.corpus
shuf corpus.txt | awk '{print; print "<stop>"}' >> corpus.1.corpus
./auto_corpus.sh >> corpus.1.corpus
# Include LLM-expanded rewrites if they exist
if [ -f llm_expanded_corpus.txt ]; then
    cat llm_expanded_corpus.txt >> corpus.1.corpus
fi
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

pushd .
cd level_5/
# Start with previous levels
cat ../level_4/corpus.corpus > corpus.corpus

# Non-JSON level_5 content: all files (no format tag)
for dir in sentence_analysis conjugations english spanish french italian portuguese tables word_problems; do
    for f in $(find corpus/$dir -name '*.corpus' -type f 2>/dev/null | sort); do
        cat "$f" >> corpus.corpus
        echo '<stop>' >> corpus.corpus
    done
done

# json_qa / json_qa_2: 3-line blocks (Context / Input / Output) + blank separator.
# Do NOT use [json] prefix here — the 3-line format conflicts with the 2-line
# json_instruction format and trains the model to output "Context:" after [json].
for dir in json_qa json_qa_2; do
    for f in $(find corpus/$dir -name '*.corpus' -type f 2>/dev/null | sort); do
        cat "$f" >> corpus.corpus
        echo '<stop>' >> corpus.corpus
    done
done

# json_instruction: true 2-line pairs (prompt / JSON answer) with blank separators.
# Strip blank lines first so NR%2 aligns correctly regardless of separators.
for dir in json_instruction; do
    for f in $(find corpus/$dir -name '*.corpus' -type f 2>/dev/null | sort); do
        grep -v '^$' "$f" | awk 'NR%2==1{print "[json] " $0} NR%2==0{print; print "<stop>"}' >> corpus.corpus
    done
done

# Tool-use API calls: sample to ~15% of total corpus lines.
# Non-tool-use lines so far ≈ level4(52625) + sentence_analysis(15002) +
# json_qa(9939) + conjugations(6772) + other(6459) ≈ 90797.
# Target: tool_use_lines / (90797 + tool_use_lines) = 0.15
#   => tool_use_lines ≈ 16023. Current files avg ~57 lines → need ~281 files.
# We sample 30% of all tool_use + tool_use_2 files (904 total → ~271 files).
ALL_TOOL_USE=$(find corpus/tool_use corpus/tool_use_2 -name '*.corpus' -type f 2>/dev/null)
TOOL_USE_COUNT=$(echo "$ALL_TOOL_USE" | wc -l)
TOOL_USE_SAMPLE=$(( TOOL_USE_COUNT * 30 / 100 ))
echo "Sampling $TOOL_USE_SAMPLE / $TOOL_USE_COUNT tool_use files (~15% of total lines)"
echo "$ALL_TOOL_USE" | shuf | head -n "$TOOL_USE_SAMPLE" | sort | while read f; do
    # Prefix each Question: line with [json] so the model gates on that token
    sed 's/^Question:/[json] Question:/' "$f" >> corpus.corpus
    echo '<stop>' >> corpus.corpus
done

du -h corpus.corpus
popd
