# 🚀 InfinityFree Deployment Checklist

**Use this checklist every time you deploy changes to InfinityFree**

---

## 📋 **Before Deployment**

- [ ] All changes tested locally on XAMPP
- [ ] Database works correctly on localhost
- [ ] No errors in browser console
- [ ] All features working as expected

---

## 🔄 **Deployment Steps**

### **1. Prepare Files**

- [ ] **Identify changed files** (check LastWriteTime or git status)
- [ ] **Review config files** - Make sure NO localhost settings!
- [ ] **Check for VIEWs** - Remove any CREATE VIEW statements from SQL

### **2. Handle Config Files**

#### **Option A: Use separate production config**
```bash
# Upload db_production.php and rename it to db.php on server
# This keeps your local config intact
```

#### **Option B: Temporarily change config**
```bash
# Change config/db.php to InfinityFree settings
# Upload to server
# Change back to localhost after upload
```

**Recommended:** Use Option A (separate file)

---

### **3. Upload via FTP**

**FTP Connection:**
- Host: `ftpupload.net`
- Port: `21`
- Username: `epiz_39888624` (or your InfinityFree username)
- Password: Your InfinityFree FTP password

**Upload these if changed:**
- [ ] PHP files (dashboard.php, patients.php, etc.)
- [ ] CSS files (assets/css/)
- [ ] JavaScript files (assets/js/)
- [ ] config/db.php (production version!)
- [ ] New images/assets if any

**DO NOT upload:**
- ❌ .git folder
- ❌ archive folder
- ❌ database folder (SQL files)
- ❌ Local config with localhost settings

---

### **4. Database Changes (If Needed)**

**Only if you changed database structure!**

- [ ] Export from XAMPP phpMyAdmin
- [ ] **Remove all CREATE VIEW statements**
- [ ] **Remove DEFINER clauses**
- [ ] Test SQL file locally first
- [ ] Import to InfinityFree phpMyAdmin

**If only data changed:**
- [ ] Export just the data (INSERT statements)
- [ ] Import to InfinityFree

---

### **5. Verify Deployment**

- [ ] Visit: http://patty-portfolio.infinityfree.me
- [ ] Login with admin/admin123
- [ ] Test the feature you changed
- [ ] Check browser console for errors
- [ ] Test on mobile (responsive)

---

## 🔧 **Quick Commands**

### **Check what files changed:**
```powershell
# Files changed in last 24 hours
Get-ChildItem -Path "c:\Users\SHC\Desktop\careApp\webapp" -Recurse -File | Where-Object {$_.LastWriteTime -gt (Get-Date).AddDays(-1)} | Select-Object FullName, LastWriteTime
```

### **Sync to XAMPP:**
```powershell
xcopy "c:\Users\SHC\Desktop\careApp\webapp\*.*" "c:\xampp\htdocs\webapp\" /D /E /Y /I
```

### **Git commit:**
```bash
cd c:\Users\SHC\Desktop\careApp
git add .
git commit -m "Description of changes"
git push origin main
```

---

## 🐛 **Troubleshooting After Deployment**

### **If you see HTTP 500:**
1. Upload `test_connection.php`
2. Visit: http://patty-portfolio.infinityfree.me/test_connection.php
3. Check which test fails
4. Fix the issue and re-upload

### **If database connection fails:**
1. Verify `config/db.php` has InfinityFree credentials
2. Check password is correct (get from InfinityFree panel)
3. Verify database exists on InfinityFree

### **If features not working:**
1. Check browser console for JavaScript errors
2. Check if API endpoint is correct (Render.com URL)
3. Verify all required files uploaded

---

## 📁 **File Upload Reference**

### **Always upload these if changed:**
```
htdocs/
├── config/
│   └── db.php (production version!)
├── *.php (any changed files)
└── assets/ (if CSS/JS changed)
```

### **Never upload these:**
```
❌ .git/
❌ .venv/
❌ archive/
❌ database/ (local SQL files)
❌ test files
❌ backup files
```

---

## ✅ **Post-Deployment**

- [ ] Test all main features
- [ ] Check dashboard loads
- [ ] Try creating a prediction
- [ ] Verify patient list displays
- [ ] Test logout/login
- [ ] Document what was deployed (git commit message)

---

## 🔐 **Security Reminders**

- [ ] Never upload files with localhost config
- [ ] Never commit passwords to Git
- [ ] Keep production config separate from local
- [ ] Change default admin password (admin123)
- [ ] Use strong database password

---

## 📝 **Deployment Log Template**

**Date:** _____________  
**Changes Made:**
- 
- 
- 

**Files Uploaded:**
- 
- 

**Database Changes:** Yes / No  
**Tested On:** XAMPP / InfinityFree  
**Status:** ✅ Success / ❌ Issues  
**Notes:**

---

**Save this file and use it for every deployment!**
