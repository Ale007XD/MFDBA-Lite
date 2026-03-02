#!/bin/bash
> project-full-dump.md
echo "# 🎯 Полный снапшот MFDBA-Lite" >> project-full-dump.md
echo "**Commit:** $(git rev-parse HEAD) | **Файлов:** $(find . -type f | wc -l)**" >> project-full-dump.md
echo "" >> project-full-dump.md

for file in $(find . -type f ! -path '*/.git/*' | sort); do
  echo -e "
## 📄 $file" >> project-full-dump.md
  echo "**Размер:** $(wc -c < "$file") bytes | $(file "$file")**" >> project-full-dump.md
  echo "```" >> project-full-dump.md
  if file "$file" | grep -q text; then
    cat "$file" >> project-full-dump.md 2>/dev/null
  else
    echo "[Binary file]" >> project-full-dump.md
  fi
  echo -e "
```
" >> project-full-dump.md
done
echo -e "
**✅ Генерация завершена:** $(date)" >> project-full-dump.md
