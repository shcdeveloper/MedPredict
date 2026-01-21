# Complete Free Deployment Guide

## 🎯 Full Stack Deployment (100% FREE)

This guide shows how to deploy your entire Healthcare Prediction System for **$0/month**.

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────┐
│                    USER                             │
└─────────────────────┬───────────────────────────────┘
                      │
        ┌─────────────┴─────────────┐
        │                           │
        ▼                           ▼
┌───────────────┐           ┌──────────────┐
│  PHP Frontend │           │  FastAPI     │
│  InfinityFree │◄─────────►│  Render.com  │
│               │   API     │              │
└───────┬───────┘  Calls    └──────┬───────┘
        │                          │
        │    ┌─────────────────────┘
        │    │
        ▼    ▼
┌─────────────────┐
│  MySQL Database │
│  InfinityFree   │
└─────────────────┘
```

---

## Part 1: Deploy FastAPI (Render.com)

### Prerequisites
- GitHub account
- Code in GitHub repository

### Steps

#### 1. Create `render.yaml`
```yaml
services:
  - type: web
    name: healthcare-api
    env: python
    region: oregon
    plan: free
    buildCommand: |
      pip install -r requirements.txt
      python -m api.train_model
    startCommand: uvicorn api.main:app --host 0.0.0.0 --port $PORT
    healthCheckPath: /health
    envVars:
      - key: PYTHON_VERSION
        value: 3.11.0
```

#### 2. Update CORS in `api/main.py`
```python
# Allow your InfinityFree domain
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://yoursite.infinityfree.com",
        "http://yoursite.infinityfree.com"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

#### 3. Deploy
1. Go to https://render.com
2. Sign up with GitHub (free)
3. New Web Service → Connect repo
4. Use Free tier
5. Deploy!

**Result**: API at `https://healthcare-api-xxxx.onrender.com`

---

## Part 2: Deploy PHP + MySQL (InfinityFree)

### Step 1: Create InfinityFree Account

1. Go to https://infinityfree.com
2. Sign up (free, no credit card)
3. Create account (choose subdomain: `yoursite.infinityfree.com`)

### Step 2: Upload PHP Files

#### Option A: File Manager (Easy)
1. Login to control panel
2. Go to "File Manager"
3. Navigate to `/htdocs/`
4. Upload your `webapp/` folder contents
5. Make sure `index.php` or `login.php` is in root

#### Option B: FTP (Recommended)
1. Get FTP credentials from control panel
2. Use FileZilla or WinSCP
3. Upload to `/htdocs/`

**FTP Settings**:
```
Host: ftpupload.net (or ftp.yoursite.infinityfree.com)
Username: (from control panel)
Password: (from control panel)
Port: 21
```

### Step 3: Setup MySQL Database

1. Control Panel → MySQL Databases
2. Create database
3. Note credentials:
   ```
   Server: sql123.infinityfree.com
   Database: epiz_12345678_healthcare
   Username: epiz_12345678
   Password: (your password)
   Port: 3306
   ```

### Step 4: Import Database

1. Go to phpMyAdmin (link in control panel)
2. Select your database
3. Click "Import"
4. Upload `database/setup.sql`
5. Click "Go"

### Step 5: Update Database Config

Edit `webapp/config/db.php`:
```php
<?php
$host = 'sql123.infinityfree.com';  // From InfinityFree
$dbname = 'epiz_12345678_healthcare';
$username = 'epiz_12345678';
$password = 'your_password';
$port = 3306;

try {
    $pdo = new PDO("mysql:host=$host;port=$port;dbname=$dbname", $username, $password);
    $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
} catch(PDOException $e) {
    die("Connection failed: " . $e->getMessage());
}

function getDBConnection() {
    global $pdo;
    return $pdo;
}
?>
```

### Step 6: Update API Endpoint

Create `webapp/config/api.php`:
```php
<?php
// Point to your Render API
define('API_BASE_URL', 'https://healthcare-api-xxxx.onrender.com');
define('API_PREDICT_ENDPOINT', API_BASE_URL . '/predict');
define('API_DISEASE_ENDPOINT', API_BASE_URL . '/predict-disease');
define('API_HEALTH_ENDPOINT', API_BASE_URL . '/health');
?>
```

Update `webapp/submit_prediction.php`:
```php
<?php
require_once 'config/api.php';

// Replace hardcoded URL with:
$ch = curl_init(API_PREDICT_ENDPOINT);
```

---

## Part 3: Connect Everything

### Update Render Environment Variables

In Render dashboard → Environment:
```
DB_HOST=sql123.infinityfree.com
DB_USER=epiz_12345678
DB_PASSWORD=your_password
DB_NAME=epiz_12345678_healthcare
DB_PORT=3306
```

### Test Database Connection

Create `test_db.php` on InfinityFree:
```php
<?php
require_once 'config/db.php';

try {
    $pdo = getDBConnection();
    echo "✅ Database connected successfully!";
    
    $stmt = $pdo->query("SELECT COUNT(*) FROM patient_requests");
    $count = $stmt->fetchColumn();
    echo "<br>Total patients: $count";
} catch(Exception $e) {
    echo "❌ Error: " . $e->getMessage();
}
?>
```

Visit: `https://yoursite.infinityfree.com/test_db.php`

---

## Part 4: Keep API Awake (Prevent Sleep)

### Option 1: UptimeRobot (Recommended)

1. Go to https://uptimerobot.com
2. Sign up (free)
3. Add new monitor:
   - Type: HTTP(s)
   - URL: `https://healthcare-api-xxxx.onrender.com/health`
   - Interval: 5 minutes
4. Save

**Result**: API stays awake 24/7

### Option 2: Cron-Job.org

1. Go to https://cron-job.org
2. Sign up (free)
3. Create cronjob:
   - URL: `https://healthcare-api-xxxx.onrender.com/health`
   - Interval: Every 5 minutes
4. Save

---

## Part 5: Testing

### Test API
```bash
curl https://healthcare-api-xxxx.onrender.com/health
```

### Test Web App
1. Visit `https://yoursite.infinityfree.com`
2. Login with: `admin` / `admin123`
3. Make a prediction
4. Check if it calls API successfully

### Test Full Flow
1. Open web app
2. Go to "Admission Prediction"
3. Fill form
4. Submit
5. Should see prediction result from Render API

---

## 📊 Free Tier Limits

### Render.com (API)
- ✅ 750 hours/month (24/7 coverage)
- ✅ 512 MB RAM
- ✅ 100 GB bandwidth/month
- ⚠️ Sleeps after 15 min (solved with UptimeRobot)
- ⚠️ 30-50s cold start

### InfinityFree (PHP + MySQL)
- ✅ Unlimited bandwidth
- ✅ 5 GB storage
- ✅ 400 MySQL databases
- ✅ Free subdomain
- ⚠️ Ads on control panel (not on site)
- ⚠️ Daily hits limit (50,000/day)

### UptimeRobot (Monitoring)
- ✅ 50 monitors
- ✅ 5-minute intervals
- ✅ Email alerts

**Total Cost**: **$0/month** ✨

---

## 🔒 Security Checklist

- [ ] Change default admin password
- [ ] Use environment variables for secrets
- [ ] Enable HTTPS (automatic on both platforms)
- [ ] Set CORS to specific domain only
- [ ] Use prepared statements (PDO)
- [ ] Validate all inputs
- [ ] Don't expose error details in production

---

## 🐛 Common Issues

### Issue: API Not Responding
**Solution**: 
1. Check Render logs
2. Verify UptimeRobot is active
3. Wait 50s for cold start

### Issue: Database Connection Failed
**Solution**:
1. Verify InfinityFree MySQL credentials
2. Check if remote access is enabled
3. Use correct host (not `localhost`)

### Issue: CORS Error
**Solution**:
```python
# In api/main.py
allow_origins=[
    "https://yoursite.infinityfree.com",
    "http://yoursite.infinityfree.com"  # Add http too
]
```

### Issue: Models Not Found
**Solution**: Add to `render.yaml`:
```yaml
buildCommand: |
  pip install -r requirements.txt
  python -m api.train_model
  python api/train_disease_models.py
```

---

## 📈 Performance Optimization

### For Render (API)
1. Use startup command to preload models
2. Enable health checks
3. Use UptimeRobot to keep warm
4. Cache predictions if needed

### For InfinityFree (PHP)
1. Enable OPcache (if available)
2. Minimize database queries
3. Use browser caching
4. Compress responses

---

## 🚀 Deployment Checklist

**Before Deployment**:
- [ ] Code in GitHub repository
- [ ] `render.yaml` configured
- [ ] CORS updated for InfinityFree domain
- [ ] Database credentials in environment variables

**Render Deployment**:
- [ ] Signed up for Render
- [ ] Connected GitHub repo
- [ ] Selected Free tier
- [ ] Added environment variables
- [ ] Deployed successfully
- [ ] Health check passing

**InfinityFree Deployment**:
- [ ] Created account
- [ ] Uploaded PHP files
- [ ] Created MySQL database
- [ ] Imported schema
- [ ] Updated `config/db.php`
- [ ] Updated API endpoint URL

**Connection**:
- [ ] Set up UptimeRobot
- [ ] Tested API from web app
- [ ] Tested predictions end-to-end
- [ ] Verified database updates

**Final**:
- [ ] Changed default passwords
- [ ] Tested on mobile
- [ ] Checked logs for errors
- [ ] Documented access URLs

---

## 🎯 Your Live URLs

After deployment, you'll have:

```
Web Application:  https://yoursite.infinityfree.com
API:              https://healthcare-api-xxxx.onrender.com
API Docs:         https://healthcare-api-xxxx.onrender.com/docs
phpMyAdmin:       (link in InfinityFree control panel)
```

---

## 📞 Support Resources

**Render**:
- Docs: https://render.com/docs
- Community: https://community.render.com
- Status: https://status.render.com

**InfinityFree**:
- Forum: https://forum.infinityfree.com
- Support: Submit ticket in control panel

---

## 💡 Pro Tips

1. **Custom Domain** (optional):
   - Buy domain ($1/year on Namecheap)
   - Point to InfinityFree
   - Use Cloudflare for free SSL

2. **Backup**:
   - Export database weekly
   - Keep code in GitHub
   - Download files monthly

3. **Monitoring**:
   - Use UptimeRobot for API
   - Use Google Analytics for traffic
   - Check logs regularly

4. **Performance**:
   - First request after sleep: 30-50s
   - Normal requests: < 200ms
   - Accept trade-off for free hosting

---

## 🎓 For Your Portfolio

**What to Show**:
- Live demo URL
- GitHub repository
- API documentation
- Architecture diagram
- Free hosting strategy

**What to Mention**:
- "Deployed production-ready ML system for $0/month"
- "Implemented auto-deploy pipeline with GitHub + Render"
- "Optimized for free tier constraints with UptimeRobot"
- "Full-stack deployment: Python API + PHP frontend + MySQL"

---

**Congratulations! Your app is now live and FREE!** 🎉

**Share these URLs in your resume/portfolio** 🚀
