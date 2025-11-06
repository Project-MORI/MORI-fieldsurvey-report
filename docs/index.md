cat > index.md <<'EOF'
# MORI Field Survey Report

初期テストページです。Obsidianで編集 → Git push → 自動公開されます。
EOF


git add -A

git commit -m "fix: move docs under docs/ and use default docs_dir"

git push