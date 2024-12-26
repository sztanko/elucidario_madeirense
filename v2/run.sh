CHUNK_SIZE=50000

# Step 1: convert pdfs to text
../.venv/bin/markitdown ../source/vol_1.pdf > vol_1.md
../.venv/bin/markitdown ../source/vol_2.pdf > vol_2.md
../.venv/bin/markitdown ../source/vol_3.pdf > vol_3.md

# Step 2: preprocess
cat vol_*.md | python ops.py preprocess > p.txt # this is just for illustration purposes, p.txt is not used in the next steps

# Step 3: chunk
# cat vol_*.md | python ops.py chunks --chunk-size $CHUNK_SIZE > chunks.json

cat vol_*.md | python ops.py structure-all --chunk-size $CHUNK_SIZE structure.yaml

