#!/bin/bash

# Regulatory Reporting Automation - Deployment Script

echo "🚀 Deploying Regulatory Reporting Automation to GitHub and Vercel"
echo "============================================================"

# Check if git is initialized
if [ ! -d .git ]; then
    echo "📦 Initializing git repository..."
    git init
fi

# Add all files
echo "📝 Adding files to git..."
git add .

# Commit
echo "💾 Creating initial commit..."
git commit -m "feat: initial commit - regulatory reporting automation MVP" || echo "No changes to commit"

# Check if remote exists
if ! git remote | grep -q "origin"; then
    echo "🔗 Adding GitHub remote..."
    git remote add origin https://github.com/johnnycchung/regulatory-reporting-automation.git
fi

# Push to GitHub
echo "📤 Pushing to GitHub..."
git branch -M main
git push -u origin main

echo ""
echo "✅ GitHub deployment complete!"
echo ""
echo "📋 Next steps:"
echo "1. Go to https://vercel.com/new"
echo "2. Import the GitHub repository: johnnycchung/regulatory-reporting-automation"
echo "3. Deploy with these settings:"
echo "   - Framework Preset: Other"
echo "   - Install Command: pip install -r requirements-vercel.txt"
echo ""
echo "Or use Vercel CLI:"
echo "   npm i -g vercel"
echo "   vercel --prod"
echo ""
echo "🔗 The app will be available at:"
echo "   https://www.johnnycchung.com/regreporting"