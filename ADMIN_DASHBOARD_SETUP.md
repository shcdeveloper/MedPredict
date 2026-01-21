# 🏥 Admin Dashboard Setup Guide

## ✨ New Features Added

Your Healthcare Admission Prediction System now has a **professional admin dashboard** with:

- ✅ **User Authentication** - Secure login for clinicians and doctors
- ✅ **Role-Based Access** - Admin, Doctor, and Clinician roles
- ✅ **Professional Dashboard** - Modern, clean UI with statistics
- ✅ **Patient History** - View all predictions with search
- ✅ **User Management** - Track who made each prediction
- ✅ **Responsive Design** - Works on all devices

## 🚀 Setup Instructions

### Step 1: Run the Admin Database Setup

1. **Open phpMyAdmin**: http://localhost/phpmyadmin
2. **Click "SQL" tab**
3. **Copy and paste** the contents of: `database/setup_admin.sql`
4. **Click "Go"**

This creates:
- `admin_users` table for login accounts
- `admin_sessions` table for session management  
- Updated `patient_requests` table with user tracking
- Dashboard statistics views
- **3 default admin accounts** (see below)

### Step 2: Copy Updated Webapp to XAMPP

```powershell
# Copy the updated webapp folder
Copy-Item -Path "C:\Users\SHC\Desktop\careApp\webapp" -Destination "C:\xampp\htdocs\" -Recurse -Force
```

### Step 3: Access the New Admin Dashboard

Open your browser and go to:
```
http://localhost/webapp/login.php
```

## 👥 Default Login Credentials

### Administrator Account
- **Username:** `admin`
- **Password:** `admin123`
- **Role:** Full system access

### Doctor Account
- **Username:** `dr.smith`
- **Password:** `admin123`
- **Role:** Clinical access

### Clinician Account
- **Username:** `clinician1`
- **Password:** `admin123`
- **Role:** Standard access

## 📱 Dashboard Features

### 1. Login Page (`login.php`)
- Professional medical-themed design
- Secure authentication
- Session management

### 2. Dashboard (`dashboard.php`)
- **Statistics Overview:**
  - Total predictions
  - High/Medium/Low risk counts
  - Recent patient activity
- **Quick Actions:**
  - New prediction
  - View patients
  - Analytics
- **Recent Predictions Table:**
  - Last 10 predictions
  - Clinician tracking
  - Risk level badges

### 3. New Prediction (`predict.php`)
- **Professional Form Design:**
  - Patient demographics
  - Clinical parameters
  - Real-time validation
  - Input hints and guidelines
- **Features:**
  - Patient name tracking
  - Clinical notes (optional)
  - Risk level guidelines
  - Form validation

### 4. Patient History (`patients.php`)
- View all predictions
- Search functionality
- Filter by risk level
- Clinician attribution
- Date/time stamps

### 5. Navigation
- **Sidebar Menu:**
  - Dashboard
  - New Prediction
  - Patient History
  - Analytics
  - User Management (Admin only)
  - Settings
  - Logout

## 🎨 New Design Elements

### Professional UI Components
- **Color Scheme:**
  - Primary: Blue (#2563eb)
  - Success: Green (#10b981)
  - Warning: Orange (#f59e0b)
  - Danger: Red (#ef4444)

- **Typography:**
  - Clean, professional fonts
  - Clear hierarchy
  - Medical-appropriate styling

- **Components:**
  - Stat cards with icons
  - Badge system for risk levels
  - Professional tables
  - Modern forms
  - Alert messages

### Icons
Using Font Awesome 6.0 for professional medical icons

## 🔐 Security Features

1. **Password Hashing** - bcrypt encryption
2. **Session Management** - Secure PHP sessions
3. **Role-Based Access** - Different permissions per role
4. **Input Validation** - Both client and server-side
5. **SQL Injection Protection** - Prepared statements
6. **XSS Prevention** - HTML escaping

## 📊 Database Structure

### New Tables

#### `admin_users`
```sql
- id (Primary Key)
- username (Unique)
- password_hash
- full_name
- email
- role (doctor/clinician/admin)
- is_active
- last_login
- created_at
```

#### `admin_sessions`
```sql
- id (Primary Key)
- user_id (Foreign Key)
- session_token
- expires_at
- created_at
```

#### Updated `patient_requests`
```sql
- user_id (Foreign Key to admin_users)
- patient_name (NEW)
- ... existing fields ...
```

## 🎯 Usage Flow

1. **Login** → `login.php`
2. **View Dashboard** → `dashboard.php`
3. **Make Prediction** → `predict.php` → `submit_prediction.php`
4. **View Results** → Professional result page
5. **Check History** → `patients.php`
6. **Logout** → `logout.php`

## 📸 Page Descriptions

### Login Page
- Medical-themed design
- Gradient background
- Card-based form
- Demo credentials shown
- Secure authentication

### Dashboard
- 4 stat cards (Total, High Risk, Medium Risk, Low Risk)
- Quick action buttons
- Recent predictions table
- User profile in header
- Sidebar navigation

### Prediction Form
- Two-column layout
- Organized sections (Demographics, Clinical)
- Real-time validation hints
- Color-coded warnings
- Risk level guidelines panel
- Professional medical styling

### Result Page
- Large, clear probability display
- Color-coded risk badge
- Patient information summary
- Action buttons (New, View All, Dashboard, Print)
- Success confirmation

### Patient History
- Searchable data table
- All patient records
- Risk level badges
- Clinician attribution
- Date sorting

## 🔧 Configuration

### File Structure
```
webapp/
├── login.php                    # Login page
├── logout.php                   # Logout handler
├── dashboard.php                # Main dashboard
├── predict.php                  # Prediction form
├── submit_prediction.php        # Form handler
├── patients.php                 # Patient history
├── config/
│   ├── db.php                   # Database config
│   └── auth.php                 # Authentication functions
└── assets/
    └── css/
        └── admin.css            # Professional styling
```

### Customization

To change the hospital/system name, edit:
- Login page title
- Sidebar logo (`MedPredict`)
- Header titles

To add more admin users:
```sql
INSERT INTO admin_users (username, password_hash, full_name, email, role) 
VALUES ('newuser', '$2y$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi', 
        'Full Name', 'email@hospital.com', 'clinician');
```
(Password: admin123)

## ✅ Testing Checklist

- [ ] Database setup completed
- [ ] Webapp copied to htdocs
- [ ] Can login with admin account
- [ ] Dashboard displays correctly
- [ ] Can make new prediction
- [ ] Prediction saves to database
- [ ] Patient history shows records
- [ ] Search works in patient history
- [ ] Logout works correctly
- [ ] API server is running

## 🎉 You're Done!

Your professional admin dashboard is ready! Access it at:
**http://localhost/webapp/login.php**

Login with any of the default accounts and start managing patient predictions!

## 💡 Next Steps

1. **Customize branding** - Update hospital name and logo
2. **Add more users** - Create accounts for your team
3. **Enable HTTPS** - For production deployment
4. **Add analytics page** - Create charts and reports
5. **Implement user management** - Admin panel for user CRUD

---

**Need Help?** Check the main `SETUP_GUIDE.md` or documentation files.
