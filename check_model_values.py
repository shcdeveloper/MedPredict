"""
Quick script to check what values the disease model expects
"""
import joblib
from pathlib import Path

model_dir = Path('models/disease_models')

if model_dir.exists():
    try:
        # Load encoders
        diabetes_encoders = joblib.load(model_dir / 'diabetes_encoders.pkl')
        
        print("=" * 60)
        print("DISEASE MODEL - EXPECTED VALUES")
        print("=" * 60)
        
        for col, encoder in diabetes_encoders.items():
            print(f"\n{col.upper()}:")
            print(f"  Expected values: {list(encoder.classes_)}")
        
        print("\n" + "=" * 60)
        print("FORM VALUES SHOULD MATCH THESE EXACTLY!")
        print("=" * 60)
        
    except Exception as e:
        print(f"Error: {e}")
        print("\nYou need to retrain the model:")
        print("  python data/generate_disease_data.py")
        print("  python api/train_disease_models.py")
else:
    print("Disease models not found!")
    print("\nTrain the models:")
    print("  python data/generate_disease_data.py")
    print("  python api/train_disease_models.py")
