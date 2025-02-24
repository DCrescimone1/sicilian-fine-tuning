#!/bin/bash

# Set the output file name
output_file="fine_tuning_dump.txt"

# Define common exclusion patterns
EXCLUDE_DIRS="node_modules|.git|build|.next|venv|__pycache__|dist|coverage|.turbo|.cache|.yarn"
EXCLUDE_FILES="*.pyc|*.png|*.jpg|*.jpeg|*.gif|*.bmp|*.svg|*.ico|*.lock|.DS_Store|*.dump.txt|.env*|.gitignore|*.min.js|*.min.css|*.map|*.d.ts|*.d.cts|*.cjs|package.json|tsconfig*.json|*.tsbuildinfo|browserslist"

# Generate the tree structure with better formatting and exclusions
echo "Project Structure:" > "$output_file"
tree -L 4 --charset=ascii \
    -I "${EXCLUDE_DIRS}|${EXCLUDE_FILES}" 2>/dev/null | while IFS= read -r line; do
    # Replace the default tree characters with more readable ones
    line=$(echo "$line" | sed 's/|--/├──/g' | sed 's/`--/└──/g')
    echo "$line" >> "$output_file"
done

# Add a separator
echo -e "\n\n--- File Contents ---\n" >> "$output_file"

# Find and dump only source code files
find . \( \
    -name "*.ts" -o \
    -name "*.tsx" -o \
    -name "*.js" -o \
    -name "*.jsx" -o \
    -name "*.css" -o \
    -name "*.scss" -o \
    -name "*.html" -o \
    -name "*.sql" -o \
    -name "*.md" \
    \) \
    ! -path "*/node_modules/*" \
    ! -path "*/.git/*" \
    ! -path "*/build/*" \
    ! -path "*/.next/*" \
    ! -path "*/dist/*" \
    ! -path "*/coverage/*" \
    ! -path "*/.turbo/*" \
    ! -path "*/.cache/*" \
    ! -path "*/__pycache__/*" \
    ! -path "*/.yarn/*" \
    ! -name "*.min.js" \
    ! -name "*.min.css" \
    ! -name "*.map" \
    ! -name "*.d.ts" \
    ! -name "*.d.cts" \
    ! -name "*.cjs" \
    ! -name "*.csv" \
    -print0 | sort -z | while IFS= read -r -d '' file; do
    # Check if the file is not empty and is readable
    if [ -s "$file" ] && [ -r "$file" ]; then
        echo -e "\n------------------------------------------------- $file --------------------------------------------------\n" >> "$output_file"
        cat "$file" >> "$output_file"
    fi
done

echo "Dump completed. Output saved to $output_file"