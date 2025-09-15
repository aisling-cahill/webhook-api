# Complete API Setup Guide

## Prerequisites
- You already have the code and dependencies installed ✅
- You need your Supabase database connection details

## Step 1: Get Your Supabase Connection String

1. **Go to Supabase Dashboard**
   - Open your browser
   - Go to https://supabase.com
   - Click "Sign in" and log into your account
   - Select your project

2. **Find Database Settings**
   - Click on "Settings" in the left sidebar
   - Click on "Database"
   - Scroll down to "Connection string"

3. **Copy the Connection String**
   - Look for "Nodejs" connection string
   - It looks like: `postgresql://postgres:[YOUR-PASSWORD]@db.[YOUR-PROJECT-REF].supabase.co:5432/postgres`
   - Copy this entire string
   - **Important**: Replace `[YOUR-PASSWORD]` with your actual database password

## Step 2: Create Environment File

1. **In Terminal, run these commands:**
   ```bash
   cd /Users/aislingcahill/webhook-api
   cp .env.example .env
   ```

2. **Edit the .env file:**
   ```bash
   open .env
   ```

   This opens the file. Replace the contents with:
   ```
   DATABASE_URL=postgresql://postgres:YOUR_ACTUAL_PASSWORD@db.YOUR_PROJECT_REF.supabase.co:5432/postgres
   ```

## Step 3: Test Your API

1. **Start the server:**
   ```bash
   python3 main.py
   ```

2. **Test the health endpoint:**
   - Open a new browser tab
   - Go to: http://localhost:8000/health
   - You should see: `{"status":"healthy"}`

3. **View API documentation:**
   - Go to: http://localhost:8000/docs
   - This shows interactive API documentation

## Step 4: Test with Real Data

Use the sample webhook data to test:

```bash
curl -X POST "http://localhost:8000/telnyx-dynamic-vars" \
  -H "Content-Type: application/json" \
  -d '{
    "data": {
      "payload": {
        "telnyx_end_user_target": "+353857688030"
      }
    }
  }'
```

## Step 5: Production Deployment

Choose one of these options:

### Option A: Railway (Recommended for beginners)
1. Go to https://railway.app
2. Sign up with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Connect your GitHub and push this code
5. Add environment variable `DATABASE_URL` in Railway dashboard

### Option B: Heroku
1. Install Heroku CLI: https://devcenter.heroku.com/articles/heroku-cli
2. Login: `heroku login`
3. Create app: `heroku create your-app-name`
4. Add config: `heroku config:set DATABASE_URL="your-connection-string"`
5. Deploy: `git push heroku main`

### Option C: DigitalOcean App Platform
1. Go to https://cloud.digitalocean.com/apps
2. Create new app from GitHub
3. Add environment variable `DATABASE_URL`

## Troubleshooting

**Database Connection Error?**
- Double-check your password in the connection string
- Make sure your IP is allowed in Supabase (Settings → Database → Network restrictions)

**Import Errors?**
- Make sure you're in the right directory: `cd /Users/aislingcahill/webhook-api`
- Verify dependencies: `pip list | grep fastapi`

**Can't Access http://localhost:8000?**
- Make sure the server is running
- Try http://127.0.0.1:8000 instead
- Check if another service is using port 8000
