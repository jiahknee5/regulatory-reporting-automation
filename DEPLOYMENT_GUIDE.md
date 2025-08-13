# Deployment Guide - Regulatory Reporting Automation

## 🚀 Deployment to GitHub and Vercel

### Prerequisites
- GitHub account
- Vercel account
- Git installed locally

### Step 1: Initialize Git Repository

```bash
cd /Volumes/project_chimera/projects/regulatory-reporting-automation
git init
git add .
git commit -m "feat: initial commit - regulatory reporting automation MVP"
```

### Step 2: Create GitHub Repository

1. Go to https://github.com/new
2. Repository name: `regulatory-reporting-automation`
3. Description: "AI-powered regulatory reporting automation system"
4. Make it public
5. Don't initialize with README (we already have one)

### Step 3: Push to GitHub

```bash
git remote add origin https://github.com/johnnycchung/regulatory-reporting-automation.git
git branch -M main
git push -u origin main
```

### Step 4: Deploy to Vercel

#### Option A: Using Vercel CLI
```bash
npm i -g vercel
vercel --prod
```

#### Option B: Using Vercel Dashboard
1. Go to https://vercel.com/new
2. Import the GitHub repository
3. Configure:
   - Framework Preset: Other
   - Root Directory: ./
   - Build Command: (leave empty)
   - Output Directory: (leave empty)
   - Install Command: `pip install -r requirements-vercel.txt`

### Step 5: Configure Custom Domain

1. In Vercel dashboard, go to Settings > Domains
2. Add domain: `www.johnnycchung.com`
3. Add redirect: `/regreporting`

### Step 6: Environment Variables (if needed)

In Vercel dashboard, add:
```
PYTHON_VERSION=3.9
VERCEL=1
```

### Step 7: Set up GitHub Secrets for CI/CD

In GitHub repository settings > Secrets:
- `VERCEL_TOKEN`: Get from https://vercel.com/account/tokens
- `VERCEL_ORG_ID`: Get from Vercel dashboard
- `VERCEL_PROJECT_ID`: Get after first deployment

## 🔗 Access Points

Once deployed:
- Main site: https://www.johnnycchung.com/regreporting
- API docs: https://www.johnnycchung.com/regreporting/docs
- Health check: https://www.johnnycchung.com/regreporting/health
- API endpoints: https://www.johnnycchung.com/regreporting/api/v1/

## 🛠️ Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run locally
python src/main.py

# Access at http://localhost:8000
```

## 📝 Updating the Deployment

After making changes:
```bash
git add .
git commit -m "feat: your changes"
git push origin main
```

Vercel will automatically redeploy.

## 🐛 Troubleshooting

### Import Errors
The code handles different import paths for local vs Vercel deployment automatically.

### Path Issues
The app uses `root_path="/regreporting"` when deployed to handle subdirectory routing.

### Dependencies
Use `requirements-vercel.txt` for minimal deployment dependencies.

## 🔒 Security Notes

- Don't commit `.env` files
- Use Vercel environment variables for secrets
- Enable CORS only for trusted domains in production
- Add rate limiting for production use

## 📊 Monitoring

- Check Vercel dashboard for:
  - Function logs
  - Error tracking
  - Performance metrics
  - Usage statistics

## 🎯 Next Steps

1. Add authentication
2. Connect to real regulatory APIs
3. Implement the AI agents
4. Add production database
5. Set up monitoring alerts