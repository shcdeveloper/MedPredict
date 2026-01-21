# Deploy to Render.com (FREE)

## 🆓 Free FastAPI Deployment - No Credit Card Required

Render.com offers **750 free hours/month** which is enough for one API running 24/7.

---

## 📋 Prerequisites

- GitHub account
- Your code pushed to GitHub repository

---

## 🚀 Step-by-Step Deployment

### Step 1: Prepare Your Repository

#### 1.1 Create `render.yaml` in project root

```yaml
# render.yaml
services:
  - type: web
    name: healthcare-api
    env: python
    region: oregon
    plan: free
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn api.main:app --host 0.0.0.0 --port $PORT
    healthCheckPath: /health
    envVars:
      - key: PYTHON_VERSION
        value: 3.11.0
      - key: PORT
        value: 8000
```

#### 1.2 Update `api/main.py` to use PORT env variable

Add this at the top of `api/main.py`:

```python
import os

# Get port from environment (Render sets this)
PORT = int(os.getenv("PORT", 8000))
```

#### 1.3 Create `runtime.txt` (optional, specifies Python version)

```
python-3.11.0
```

#### 1.4 Push to GitHub

```bash
git add .
git commit -m "Add Render deployment config"
git push origin main
```

---

### Step 2: Deploy on Render

#### 2.1 Create Render Account
1. Go to https://render.com
2. Sign up with GitHub (free, no credit card)
3. Authorize Render to access your repositories

#### 2.2 Create New Web Service
1. Click "New +" → "Web Service"
2. Connect your GitHub repository
3. Select your `careApp` repository

#### 2.3 Configure Service
Render will auto-detect settings from `render.yaml`, but verify:

**Settings**:
- **Name**: `healthcare-api`
- **Environment**: `Python 3`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `uvicorn api.main:app --host 0.0.0.0 --port $PORT`
- **Plan**: `Free`

#### 2.4 Add Environment Variables
Go to "Environment" tab and add:

```
DB_HOST=sql123.infinityfree.com
DB_USER=your_infinity_user
DB_PASSWORD=your_infinity_password
DB_NAME=your_db_name
DEBUG=False
```

**Note**: You'll get these from InfinityFree after setting up MySQL.

#### 2.5 Deploy
1. Click "Create Web Service"
2. Wait 5-10 minutes for build
3. Your API will be live at: `https://healthcare-api-xxxx.onrender.com`

---

### Step 3: Test Deployment

```bash
# Health check
curl https://healthcare-api-xxxx.onrender.com/health

# API docs
# Open in browser: https://healthcare-api-xxxx.onrender.com/docs

# Test prediction
curl -X POST https://healthcare-api-xxxx.onrender.com/predict \
  -H "Content-Type: application/json" \
  -d '{
    "age": 65,
    "gender": "M",
    "heart_rate": 95,
    "glucose": 140.5,
    "prior_admission": 2
  }'
```

---

## 🔧 Configure InfinityFree to Use Render API

### Update PHP API Endpoint

In `webapp/config/api.php` (create if doesn't exist):

```php
<?php
// API Configuration
define('API_BASE_URL', 'https://healthcare-api-xxxx.onrender.com');
define('API_PREDICT_ENDPOINT', API_BASE_URL . '/predict');
define('API_DISEASE_ENDPOINT', API_BASE_URL . '/predict-disease');
define('API_HEALTH_ENDPOINT', API_BASE_URL . '/health');
```

Update `submit_prediction.php` to use this:

```php
<?php
require_once 'config/api.php';

// Use API_PREDICT_ENDPOINT instead of hardcoded URL
$ch = curl_init(API_PREDICT_ENDPOINT);
// ... rest of code
```

---

## ⚠️ Important Notes

### Free Tier Limitations

**Sleep Mode**:
- API sleeps after **15 minutes** of inactivity
- First request after sleep takes **30-50 seconds** (cold start)
- Subsequent requests are fast (< 100ms)

**Solutions**:
1. **Use a ping service** (keep awake):
   - https://uptimerobot.com (free, pings every 5 min)
   - https://cron-job.org (free scheduled requests)

2. **Accept cold starts** (acceptable for portfolio/demo)

3. **Upgrade to paid** ($7/month for no sleep)

---

### Bandwidth & Resources
- **Free tier**: 750 hours/month (enough for 24/7)
- **RAM**: 512 MB
- **Disk**: 1 GB
- **Bandwidth**: 100 GB/month
- **Build time**: 15 min max

---

## 🔄 Auto-Deploy on Git Push

Render automatically redeploys when you push to GitHub:

```bash
# Make changes
git add .
git commit -m "Update model"
git push origin main

# Render auto-detects and redeploys in ~5 minutes
```

**View logs**: Render dashboard → Your service → Logs

---

## 🐛 Troubleshooting

### Build Fails

**Problem**: `ERROR: Could not find a version that satisfies the requirement`

**Solution**: Check `requirements.txt` compatibility
```bash
# Remove version pins that cause issues
# Change: scikit-learn==1.3.0
# To:     scikit-learn>=1.3.0
```

---

### Models Not Found

**Problem**: `FileNotFoundError: models/admission_model.pkl`

**Solution**: Train models during build
```yaml
# In render.yaml, update buildCommand:
buildCommand: |
  pip install -r requirements.txt
  python -m api.train_model
  python api/train_disease_models.py
```

**Note**: This adds 2-3 minutes to build time but ensures models exist.

---

### Database Connection Error

**Problem**: `Can't connect to MySQL`

**Solution**: Update to InfinityFree remote MySQL host
```python
# In api/main.py or config
DB_HOST = "sql123.infinityfree.com"  # Not "localhost"
```

---

### API Timeout

**Problem**: Requests timing out

**Solution**: 
1. Check Render logs for errors
2. Ensure health check endpoint works
3. Reduce model complexity if needed

---

## 📊 Monitoring Your Deployment

### Render Dashboard
- **Metrics**: CPU, Memory, Response time
- **Logs**: Real-time application logs
- **Events**: Deploy history, errors

### Add Health Check Monitoring

Use your `monitoring.py` script:

```bash
# Monitor deployed API
python monitoring.py --api-url https://healthcare-api-xxxx.onrender.com
```

---

## 💰 Cost Breakdown

**Free Tier**:
- API: $0/month (750 hours)
- Database: Use InfinityFree MySQL ($0)
- Total: **$0/month**

**Paid Upgrade** (if needed):
- API: $7/month (no sleep, more RAM)
- PostgreSQL: $7/month (if needed)

---

## 🔒 Security Best Practices

1. **Never commit secrets**:
   ```bash
   # Add to .gitignore
   .env
   *.pkl  # Don't commit large model files
   ```

2. **Use Environment Variables** in Render dashboard

3. **Enable HTTPS** (automatic on Render)

4. **Add CORS restrictions**:
   ```python
   # In api/main.py
   app.add_middleware(
       CORSMiddleware,
       allow_origins=["https://yoursite.infinityfree.com"],
       allow_credentials=True,
       allow_methods=["*"],
       allow_headers=["*"],
   )
   ```

---

## 🚀 Next Steps

1. ✅ Deploy API to Render
2. ✅ Deploy PHP to InfinityFree
3. ✅ Connect them via API calls
4. ✅ Set up UptimeRobot to prevent sleep
5. ✅ Test end-to-end workflow

---

## 📞 Support

- **Render Docs**: https://render.com/docs
- **Community**: https://community.render.com
- **Status**: https://status.render.com

---

**Your API will be live at**: `https://healthcare-api-xxxx.onrender.com` 🚀

**Free, professional, and portfolio-ready!** ✨
