"""
Populate Database with 100 Sample Patient Requests and Disease Risk Assessments
================================================================================
Generates realistic patient data with corresponding disease predictions
"""

import mysql.connector
import random
from datetime import datetime, timedelta
import numpy as np

# Database connection
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="healthcare_admission"
    )

# Sample data pools
FIRST_NAMES = [
    "James", "Mary", "John", "Patricia", "Robert", "Jennifer", "Michael", "Linda",
    "William", "Elizabeth", "David", "Barbara", "Richard", "Susan", "Joseph", "Jessica",
    "Thomas", "Sarah", "Charles", "Karen", "Christopher", "Nancy", "Daniel", "Lisa",
    "Matthew", "Betty", "Anthony", "Margaret", "Mark", "Sandra", "Donald", "Ashley",
    "Steven", "Kimberly", "Paul", "Emily", "Andrew", "Donna", "Joshua", "Michelle",
    "Kenneth", "Carol", "Kevin", "Amanda", "Brian", "Dorothy", "George", "Melissa",
    "Edward", "Deborah", "Ronald", "Stephanie", "Timothy", "Rebecca", "Jason", "Sharon",
    "Jeffrey", "Laura", "Ryan", "Cynthia", "Jacob", "Kathleen", "Gary", "Amy",
    "Nicholas", "Shirley", "Eric", "Angela", "Jonathan", "Helen", "Stephen", "Anna",
    "Larry", "Brenda", "Justin", "Pamela", "Scott", "Nicole", "Brandon", "Emma",
    "Benjamin", "Samantha", "Samuel", "Katherine", "Raymond", "Christine", "Gregory", "Debra",
    "Frank", "Rachel", "Alexander", "Catherine", "Patrick", "Carolyn", "Jack", "Janet"
]

LAST_NAMES = [
    "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis",
    "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson", "Thomas",
    "Taylor", "Moore", "Jackson", "Martin", "Lee", "Perez", "Thompson", "White",
    "Harris", "Sanchez", "Clark", "Ramirez", "Lewis", "Robinson", "Walker", "Young",
    "Allen", "King", "Wright", "Scott", "Torres", "Nguyen", "Hill", "Flores",
    "Green", "Adams", "Nelson", "Baker", "Hall", "Rivera", "Campbell", "Mitchell",
    "Carter", "Roberts", "Gomez", "Phillips", "Evans", "Turner", "Diaz", "Parker",
    "Cruz", "Edwards", "Collins", "Reyes", "Stewart", "Morris", "Morales", "Murphy",
    "Cook", "Rogers", "Gutierrez", "Ortiz", "Morgan", "Cooper", "Peterson", "Bailey",
    "Reed", "Kelly", "Howard", "Ramos", "Kim", "Cox", "Ward", "Richardson"
]

SYMPTOMS = [
    "Chest pain", "Shortness of breath", "Persistent cough", "High fever",
    "Severe headache", "Abdominal pain", "Dizziness", "Fatigue",
    "Joint pain", "Nausea", "Difficulty breathing", "Irregular heartbeat",
    "Chronic back pain", "Severe allergic reaction", "Confusion",
    "Numbness in limbs", "Blurred vision", "Excessive thirst"
]

MEDICAL_HISTORY = [
    "Hypertension", "Type 2 Diabetes", "Asthma", "Previous heart surgery",
    "Kidney disease", "Arthritis", "Previous stroke", "COPD",
    "High cholesterol", "Thyroid disorder", "Cancer survivor", "Migraine disorder"
]

MEDICATIONS = [
    "Lisinopril", "Metformin", "Atorvastatin", "Amlodipine", "Levothyroxine",
    "Omeprazole", "Albuterol", "Gabapentin", "Losartan", "Sertraline",
    "Insulin", "Aspirin", "Warfarin", "Prednisone", "Ibuprofen"
]

def generate_vital_signs(age, has_condition):
    """Generate realistic vital signs based on age and health condition"""
    
    # Blood pressure (systolic/diastolic)
    if has_condition:
        systolic = random.randint(140, 180)
        diastolic = random.randint(90, 110)
    else:
        systolic = random.randint(110, 135)
        diastolic = random.randint(70, 85)
    
    # Heart rate
    base_hr = 70
    age_adjustment = (age - 40) * 0.2  # Slight increase with age
    condition_adjustment = 15 if has_condition else 0
    heart_rate = int(base_hr + age_adjustment + condition_adjustment + random.randint(-10, 10))
    heart_rate = max(55, min(120, heart_rate))
    
    # Temperature (Fahrenheit)
    if has_condition and random.random() < 0.3:
        temperature = round(random.uniform(99.5, 102.5), 1)
    else:
        temperature = round(random.uniform(97.5, 99.1), 1)
    
    # Oxygen saturation
    if has_condition:
        oxygen = random.randint(88, 96)
    else:
        oxygen = random.randint(95, 100)
    
    # Glucose (mg/dL)
    if has_condition:
        glucose = random.randint(140, 250)
    else:
        glucose = random.randint(80, 120)
    
    # BMI calculation
    if has_condition:
        bmi = round(random.uniform(27.0, 38.0), 1)
    else:
        bmi = round(random.uniform(18.5, 26.9), 1)
    
    # Cholesterol levels
    if has_condition:
        cholesterol = random.randint(220, 280)
        hdl = random.randint(30, 45)
        ldl = random.randint(140, 190)
        triglycerides = random.randint(180, 250)
    else:
        cholesterol = random.randint(150, 210)
        hdl = random.randint(50, 75)
        ldl = random.randint(80, 130)
        triglycerides = random.randint(80, 150)
    
    return {
        'blood_pressure': f"{systolic}/{diastolic}",
        'systolic': systolic,
        'diastolic': diastolic,
        'heart_rate': heart_rate,
        'temperature': temperature,
        'oxygen_saturation': oxygen,
        'glucose': glucose,
        'bmi': bmi,
        'cholesterol': cholesterol,
        'hdl': hdl,
        'ldl': ldl,
        'triglycerides': triglycerides
    }

def generate_disease_risks(age, vitals, has_history):
    """Generate disease risk assessments based on patient profile"""
    
    # Base risks
    diabetes_risk = random.uniform(0.15, 0.35) if vitals['glucose'] > 125 else random.uniform(0.05, 0.20)
    heart_risk = random.uniform(0.20, 0.45) if vitals['heart_rate'] > 90 else random.uniform(0.08, 0.25)
    hypertension_risk = random.uniform(0.25, 0.50) if vitals['systolic'] > 140 else random.uniform(0.10, 0.30)
    
    # Age adjustment
    age_factor = (age - 30) / 100
    diabetes_risk = min(0.95, diabetes_risk + age_factor)
    heart_risk = min(0.95, heart_risk + age_factor)
    hypertension_risk = min(0.95, hypertension_risk + age_factor)
    
    # History adjustment
    if has_history:
        diabetes_risk = min(0.95, diabetes_risk * 1.3)
        heart_risk = min(0.95, heart_risk * 1.3)
        hypertension_risk = min(0.95, hypertension_risk * 1.3)
    
    # Determine risk levels
    def get_risk_level(risk):
        if risk < 0.30:
            return 'Low'
        elif risk < 0.60:
            return 'Medium'
        else:
            return 'High'
    
    # Calculate overall risk
    overall_risk = (diabetes_risk + heart_risk + hypertension_risk) / 3
    
    return {
        'diabetes': round(diabetes_risk, 4),
        'diabetes_level': get_risk_level(diabetes_risk),
        'heart_disease': round(heart_risk, 4),
        'heart_disease_level': get_risk_level(heart_risk),
        'hypertension': round(hypertension_risk, 4),
        'hypertension_level': get_risk_level(hypertension_risk),
        'overall_risk': round(overall_risk, 4)
    }

def generate_admission_prediction(risks, vitals, age):
    """Generate admission prediction based on risk factors"""
    
    # Calculate risk score
    avg_risk = risks['overall_risk']
    
    # Factors increasing admission probability
    high_bp = vitals['systolic'] > 160
    high_hr = vitals['heart_rate'] > 100
    high_glucose = vitals['glucose'] > 180
    low_oxygen = vitals['oxygen_saturation'] < 92
    elderly = age > 65
    
    # Calculate admission probability
    base_probability = avg_risk * 0.6
    
    if high_bp:
        base_probability += 0.15
    if high_hr:
        base_probability += 0.10
    if high_glucose:
        base_probability += 0.12
    if low_oxygen:
        base_probability += 0.20
    if elderly:
        base_probability += 0.08
    
    admission_probability = min(0.95, base_probability)
    
    # Determine if admitted (weighted random)
    will_admit = random.random() < admission_probability
    
    return {
        'probability': round(admission_probability, 4),
        'admitted': will_admit
    }

def populate_database():
    """Main function to populate database with sample data"""
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    print("🏥 Starting database population...")
    print("=" * 70)
    
    # Clear existing sample data (optional - comment out if you want to keep existing data)
    print("\n⚠️  Clearing existing sample data...")
    # cursor.execute("DELETE FROM disease_risk_assessments WHERE patient_id LIKE 'SAMPLE%'")
    # cursor.execute("DELETE FROM patient_requests WHERE id > 0")  # Clear all if needed
    # conn.commit()
    print("✓ Keeping existing data and adding new samples")
    
    # Generate 100 patient records
    patients_added = 0
    assessments_added = 0
    
    for i in range(1, 101):
        # Generate patient info
        patient_id = f"SAMPLE{str(i).zfill(3)}"
        first_name = random.choice(FIRST_NAMES)
        last_name = random.choice(LAST_NAMES)
        age = random.randint(18, 85)
        gender = random.choice(['Male', 'Female'])
        
        # Generate contact info
        phone = f"09{random.randint(100000000, 999999999)}"
        email = f"{first_name.lower()}.{last_name.lower()}@email.com"
        
        # Generate medical data
        has_history = random.random() < 0.4  # 40% have medical history
        symptoms = random.sample(SYMPTOMS, random.randint(1, 3))
        symptoms_str = ", ".join(symptoms)
        
        medical_history_str = ""
        medications_str = ""
        if has_history:
            history_items = random.sample(MEDICAL_HISTORY, random.randint(1, 3))
            medical_history_str = ", ".join(history_items)
            meds = random.sample(MEDICATIONS, random.randint(1, 2))
            medications_str = ", ".join(meds)
        
        # Generate vital signs
        has_condition = random.random() < 0.35  # 35% have concerning vitals
        vitals = generate_vital_signs(age, has_condition)
        
        # Generate disease risks
        risks = generate_disease_risks(age, vitals, has_history)
        
        # Generate admission prediction
        admission = generate_admission_prediction(risks, vitals, age)
        
        # Random date within last 30 days
        days_ago = random.randint(0, 30)
        request_date = datetime.now() - timedelta(days=days_ago)
        
        # Determine status
        if admission['admitted']:
            status = random.choice(['admitted', 'in-treatment'])
        else:
            status = random.choice(['pending', 'reviewed', 'discharged'])
        
        # Priority based on admission probability
        if admission['probability'] > 0.7:
            priority = 'high'
        elif admission['probability'] > 0.4:
            priority = 'medium'
        else:
            priority = 'low'
        
        # Generate full patient name
        full_name = f"{first_name} {last_name}"
        
        # Insert patient request (with patient name)
        try:
            insert_request = """
            INSERT INTO patient_requests (
                patient_name, age, gender, heart_rate, glucose, prior_admission, prediction, risk_level, created_at
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            
            cursor.execute(insert_request, (
                full_name,
                age,
                gender,
                vitals['heart_rate'],
                vitals['glucose'],
                1 if has_history else 0,  # prior_admission flag
                admission['probability'],
                priority,
                request_date
            ))
            
            patients_added += 1
            request_id = cursor.lastrowid
            
            # Insert disease risk assessment with complete data
            try:
                # Generate lifestyle factors
                smoking = random.choice(['Never', 'Former', 'Current'])
                alcohol = random.choice(['None', 'Moderate', 'Heavy'])
                exercise = random.choice(['Sedentary', 'Light', 'Moderate', 'Active'])
                
                # Family history (based on has_history)
                if has_history:
                    family_diabetes = random.choice([0, 1])
                    family_heart_disease = random.choice([0, 1])
                    family_hypertension = random.choice([0, 1])
                else:
                    family_diabetes = 0
                    family_heart_disease = 0
                    family_hypertension = 0
                
                insert_assessment = """
                INSERT INTO disease_risk_assessments (
                    assessed_by, age, gender, bmi, smoking, alcohol, exercise,
                    family_diabetes, family_heart_disease, family_hypertension,
                    systolic_bp, diastolic_bp, heart_rate,
                    glucose, cholesterol, hdl, ldl, triglycerides,
                    diabetes_risk, diabetes_level,
                    heart_disease_risk, heart_disease_level,
                    hypertension_risk, hypertension_level,
                    overall_risk, created_at
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                
                cursor.execute(insert_assessment, (
                    1,  # assessed_by (user_id, default to 1)
                    age,
                    gender,
                    vitals['bmi'],
                    smoking,
                    alcohol,
                    exercise,
                    family_diabetes,
                    family_heart_disease,
                    family_hypertension,
                    vitals['systolic'],
                    vitals['diastolic'],
                    vitals['heart_rate'],
                    vitals['glucose'],
                    vitals['cholesterol'],
                    vitals['hdl'],
                    vitals['ldl'],
                    vitals['triglycerides'],
                    risks['diabetes'],
                    risks['diabetes_level'],
                    risks['heart_disease'],
                    risks['heart_disease_level'],
                    risks['hypertension'],
                    risks['hypertension_level'],
                    risks['overall_risk'],
                    request_date
                ))
                
                assessments_added += 1
            except mysql.connector.Error as e:
                # Table doesn't exist or has different structure - skip
                print(f"  ⚠️  Could not insert disease assessment: {e}")
                pass
            
            # Progress indicator
            if i % 10 == 0:
                print(f"✓ Generated {i}/100 patients...")
            
        except Exception as e:
            print(f"✗ Error inserting patient #{i}: {e}")
            continue
    
    # Commit all changes
    conn.commit()
    
    print("\n" + "=" * 70)
    print(f"✅ Database population complete!")
    print(f"   • {patients_added} patient requests added")
    print(f"   • {assessments_added} disease risk assessments added")
    
    # Show statistics
    cursor.execute("SELECT COUNT(*) FROM patient_requests")
    total_patients = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM patient_requests WHERE risk_level = 'high'")
    high_priority = cursor.fetchone()[0]
    
    cursor.execute("SELECT AVG(prediction) FROM patient_requests")
    avg_admission_prob = cursor.fetchone()[0]
    
    print(f"\n📊 Statistics:")
    print(f"   • Total patients in database: {total_patients}")
    print(f"   • High priority cases: {high_priority} ({high_priority/total_patients*100:.1f}%)")
    print(f"   • Average admission probability: {avg_admission_prob:.2%}")
    
    cursor.close()
    conn.close()
    
    print("\n🎉 You can now view the data in your dashboard!")
    print("   Visit: http://localhost/webapp/dashboard.php")

if __name__ == "__main__":
    try:
        populate_database()
    except mysql.connector.Error as err:
        print(f"\n❌ Database Error: {err}")
        print("\nMake sure:")
        print("  1. XAMPP MySQL is running")
        print("  2. Database 'healthcare_admission' exists")
        print("  3. Tables are created (run database_setup.sql)")
    except Exception as e:
        print(f"\n❌ Error: {e}")
