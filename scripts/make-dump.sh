#!/bin/bash
DUMP="snapshot-$(date +%Y%m%d-%H%M%S).md"
echo "# MFDBA-Lite $(date)" > $DUMP
echo "## Files:" >> $DUMP
find . -name "*.py" -o -name "*.toml" -o -name "*.txt" -o -name ".gitignore" | sort >> $DUMP
for f in $(find . -name "*.py" -o -name "*.toml" -o -name "*.txt"); do
 echo "" >> $DUMP
 echo "## $f" >> $DUMP
 echo '```' >> $DUMP
 cat $f >> $DUMP 2>/dev/null
 echo '```' >> $DUMP
done
git add $DUMP
git commit -m "Dump $DUMP"
git push
echo "Done: $DUMP"
