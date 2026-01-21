"""
Setup and Installation Script
Automates the initial setup of the Healthcare Admission Prediction project
"""

import os
import subprocess
import sys


def print_step(step_num, message):
    """Print formatted step message"""
    print("\n" + "="*60)
    print(f"STEP {step_num}: {message}")
    print("="*60)


def run_command(command, description):
    """Run a shell command and handle errors"""
    print(f"\n▶ {description}...")
    try:
        result = subprocess.run(
            command,
            shell=True,
            check=True,
            capture_output=True,
            text=True
        )
        print(f"✓ {description} completed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {e}")
        print(f"Output: {e.output}")
        return False


def main():
    print("\n" + "="*60)
    print("Healthcare Admission Prediction - Setup Script")
    print("="*60)
    
    # Step 1: Check Python version
    print_step(1, "Checking Python Version")
    python_version = sys.version_info
    print(f"Python {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 9):
        print("❌ Python 3.9 or higher is required")
        sys.exit(1)
    print("✓ Python version is compatible")
    
    # Step 2: Install dependencies
    print_step(2, "Installing Python Dependencies")
    if not run_command(
        f"{sys.executable} -m pip install -r requirements.txt",
        "Installing packages"
    ):
        print("⚠ Some packages may have failed to install. Please check manually.")
    
    # Step 3: Generate sample data
    print_step(3, "Generating Sample Patient Data")
    run_command(
        f"{sys.executable} data/generate_data.py",
        "Generating synthetic patient data"
    )
    
    # Step 4: Train model
    print_step(4, "Training Machine Learning Model")
    run_command(
        f"{sys.executable} -m api.train_model",
        "Training ML models"
    )
    
    # Step 5: Instructions
    print_step(5, "Setup Complete!")
    print("""
✅ Project setup completed successfully!

Next Steps:
-----------
1. Start XAMPP and enable MySQL + Apache

2. Setup Database:
   - Open phpMyAdmin (http://localhost/phpmyadmin)
   - Run the SQL script: database/setup.sql

3. Start FastAPI Server:
   cd api
   uvicorn main:app --reload

4. Deploy Web App:
   - Copy webapp/ folder to XAMPP's htdocs/
   - Access at: http://localhost/webapp/

5. Run Tests:
   pytest tests/ -v

6. Explore Notebooks:
   jupyter notebook notebooks/

For detailed instructions, see README.md
    """)


if __name__ == "__main__":
    main()
