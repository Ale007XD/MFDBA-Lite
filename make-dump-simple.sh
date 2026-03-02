#!/bin/bash
echo "# 🎯 Полный снапшот MFDBA-Lite" > project-full-dump.md
echo "**Commit:** $(git rev-parse HEAD)**" >> project-full-dump.md
echo "" >> project-full-dump.md

for file in $(find . -type f ! -path '*/.git/*' | sort); do
  echo -e "
## 📄 $file" >> project-full-dump.md
  echo "**Размер:** $(wc -c < "$file") bytes**" >> project-full-dump.md
  echo "```" >> project-full-dump.md
  cat "$file" >> project-full-dump.md 2>/dev/null
  echo -e "
```
" >> project-full-dump.md
done
echo -e "
**✅ Завершено:** $(date)" >> project-full-dump.md
