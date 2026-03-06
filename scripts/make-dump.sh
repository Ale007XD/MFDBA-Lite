#!/usr/bin/env bash
set -euo pipefail

# Папка для сохранения снапшотов (маленькими буквами — важно в Termux!)
SNAPSHOT_DIR="$HOME/storage/downloads/MFDBA-LLM-Snapshots"

mkdir -p "$SNAPSHOT_DIR" || {
    echo "Не удалось создать директорию $SNAPSHOT_DIR"
    exit 1
}

TIMESTAMP=$(date +%Y%m%d-%H%M%S 2>/dev/null)
MD_FILE="snapshot-${TIMESTAMP}.md"
JSON_FILE="snapshot-${TIMESTAMP}.json"

MD_PATH="$SNAPSHOT_DIR/$MD_FILE"
JSON_PATH="$SNAPSHOT_DIR/$JSON_FILE"

MAX_FILE_SIZE=1048576      # 1 MiB — дальше содержимое не включаем полностью
MAX_FILES_IN_JSON=120      # жёсткий лимит количества файлов в JSON

# ────────────────────────────────────────────────
# Функция — чистый список исходников (без __pycache__, .git и т.д.)
# ────────────────────────────────────────────────

get_files() {
    find . -type f \
        \(  -name "*.py"           \
         -o -name "*.toml"         \
         -o -name "pyproject.toml" \
         -o -name "*.json"         \
         -o -name "*.yaml"         \
         -o -name "*.yml"          \
         -o -name "*.md"           \
         -o -name "*.txt"          \
         -o -name "*.sh"           \
         -o -name "requirements*.txt" \
        \) \
        -not -path '*/\.*' \
        -not -path '*/__pycache__/*' \
        -not -path '*/.git/*' \
        -not -path '*/venv/*' \
        -not -path '*/.venv/*' \
        -not -path '*/.pytest_cache/*' \
        -not -path '*/.mypy_cache/*' \
        -not -path '*/node_modules/*' \
        -not -path '*/dist/*' \
        -not -path '*/build/*' \
        2>/dev/null | sort
}

# ────────────────────────────────────────────────
# Markdown-версия (читабельная для человека)
# ────────────────────────────────────────────────

{
    echo "# MFDBA-Lite Snapshot"
    echo "## $(date '+%Y-%m-%d %H:%M:%S')"
    echo "## $(pwd)"
    echo "## Файлов найдено: $(get_files | wc -l)"
    echo ""

    echo "### Список файлов"
    get_files | sed 's|^\./||; s/^/  - /'
    echo ""

    echo "### Содержимое файлов"
    echo ""

    while IFS= read -r file; do
        [ -f "$file" ] || continue

        relpath="${file#./}"
        echo "## $relpath"
        echo '```'

        case "${file##*.}" in
            py)     echo "python" ;;
            toml)   echo "toml"   ;;
            json)   echo "json"   ;;
            yml|yaml) echo "yaml" ;;
            sh)     echo "bash"   ;;
            md)     echo "markdown" ;;
        esac

        size=$(wc -c < "$file" 2>/dev/null || echo 0)

        if [ "$size" -gt "$MAX_FILE_SIZE" ]; then
            echo "# Файл слишком большой (${size} байт) — содержимое не включено"
        else
            cat "$file" 2>/dev/null || echo "# Ошибка чтения файла"
        fi

        echo '```'
        echo ""
    done < <(get_files)

    echo "---"
    echo "Создано в Termux • $(date '+%Y-%m-%d %H:%M:%S')"
} > "$MD_PATH" || {
    echo "Ошибка записи $MD_PATH"
    exit 1
}

# ────────────────────────────────────────────────
# JSON-версия с ПОЛНЫМ содержимым файлов (если они текстовые и не слишком большие)
# ────────────────────────────────────────────────

{
    echo "{"
    echo "  \"snapshot\": {"
    echo "    \"generated\": \"$(date '+%Y-%m-%d %H:%M:%S')\","
    echo "    \"directory\": \"$(pwd | sed 's/"/\\"/g')\","
    echo "    \"total_files_found\": $(get_files | wc -l),"
    echo "    \"files\": ["

    first=1
    file_idx=0

    while IFS= read -r file; do
        [ -f "$file" ] || continue
        ((file_idx++))

        if [ $file_idx -gt $MAX_FILES_IN_JSON ]; then
            break
        fi

        relpath="${file#./}"
        size=$(wc -c < "$file" 2>/dev/null || echo 0)
        escaped_path=$(echo "$relpath" | sed 's/"/\\"/g; s/\\/\\\\/g')

        if [ $first -eq 0 ]; then
            echo ","
        fi
        first=0

        echo "      {"
        echo "        \"path\": \"$escaped_path\","
        echo "        \"size_bytes\": $size,"

        if [ "$size" -gt "$MAX_FILE_SIZE" ]; then
            echo "        \"content\": \"[файл слишком большой — ${size} байт]\""
        else
            # Пытаемся экранировать содержимое как строку JSON
            content=$(cat "$file" 2>/dev/null | sed 's/\\/\\\\/g; s/"/\\"/g; s/\n/\\n/g; s/\r//g' || echo "")
            if [ -z "$content" ] && [ "$size" -gt 0 ]; then
                content="[не удалось прочитать или бинарный файл]"
            fi
            echo "        \"content\": \"$content\""
        fi

        echo "      }"
    done < <(get_files)

    echo "    ]"
    echo "  }"
    echo "}"
} > "$JSON_PATH" || {
    echo "Ошибка записи $JSON_PATH"
    exit 1
}

# ────────────────────────────────────────────────
# Делаем файлы видимыми в файловом менеджере Android
# ────────────────────────────────────────────────

if command -v termux-media-scan >/dev/null 2>&1; then
    termux-media-scan "$MD_PATH"   >/dev/null 2>&1 || true
    termux-media-scan "$JSON_PATH" >/dev/null 2>&1 || true
fi

# ────────────────────────────────────────────────
# Итог
# ────────────────────────────────────────────────

echo ""
echo "Создано:"
ls -lh "$MD_PATH" "$JSON_PATH" 2>/dev/null || echo "(файлы не найдены — проверьте права)"
echo ""
echo "Путь:  \~/storage/downloads/MFDBA-LLM-Snapshots"
echo "Файлов обработано: $(get_files | wc -l)"
echo ""
echo "Готово."
