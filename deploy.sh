#!/bin/bash
# Deploy to GitHub Pages

echo "🚀 Deploying Premium Zari Works Website..."

# Initialize git if not exists
if [ ! -d .git ]; then
    git init
fi

# Add all files
git add .

# Commit
git commit -m "Update website — $(date '+%Y-%m-%d %H:%M')"

# Push to gh-pages branch
git push origin main

echo "✅ Website deployed!"
echo "🔗 URL: https://kaifashraff.github.io/jarvis-research/zari-business/website/"
