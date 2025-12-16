
import pandas as pd
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.neighbors import KNeighborsClassifier
import joblib
import os
import sys

def main():
    """
    Trains the model on the full dataset and saves the scaler and model.
    """
    csv_path = 'feature_table.csv'
    
    # 1. Load Data
    try:
        df = pd.read_csv(csv_path)
    except FileNotFoundError:
        print(f"Error: '{csv_path}' not found.")
        print("Run 'feature_extractor.py' first!")
        sys.exit(1)

    # 2. Validation: Check for Manual Labeling
    # Ensure Class column exists and doesn't contain NaNs or empty strings
    if 'Class' not in df.columns:
        print("Error: 'Class' column missing from CSV.")
        sys.exit(1)

    # Handle empty strings that might not be NaN
    df['Class'] = df['Class'].astype(str).str.strip()
    
    # Filter for rows where Class is empty or 'nan' string (pandas artifact)
    missing_labels = df[df['Class'].isin(['', 'nan', 'None'])]
    
    if not missing_labels.empty:
        print("❌ STOP! You haven't labeled the data yet.")
        print(f"Found {len(missing_labels)} unlabeled images.")
        print("\n👉 ACTION REQUIRED:")
        print(f"1. Open '{csv_path}'")
        print("2. Fill the 'Class' column with 'Day' or 'Night'.")
        print("3. Save and re-run this script.")
        sys.exit(1)

    print(f"✅ Loaded {len(df)} labeled samples.")

    # 3. Preprocess Data
    X = df.drop(['ImageName', 'Class'], axis=1)
    y = df['Class']

    le = LabelEncoder()
    y_encoded = le.fit_transform(y)

    # 4. Feature Scaling
    # Important: Fit the scaler on the ENTIRE dataset
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # 5. Train Model
    # Train on the ENTIRE dataset
    knn = KNeighborsClassifier(n_neighbors=3)
    knn.fit(X_scaled, y_encoded)

    # 6. Save the scaler and model
    assets_dir = 'gui_app/assets'
    os.makedirs(assets_dir, exist_ok=True) # Ensure directory exists

    scaler_path = os.path.join(assets_dir, 'scaler.joblib')
    model_path = os.path.join(assets_dir, 'knn_model.joblib')

    joblib.dump(scaler, scaler_path)
    joblib.dump(knn, model_path)
    
    # Also save the label encoder classes for decoding predictions later
    le_classes_path = os.path.join(assets_dir, 'label_encoder.joblib')
    joblib.dump(le.classes_, le_classes_path)

    print(f"Scaler saved to {scaler_path}")
    print(f"Model saved to {model_path}")
    print(f"Label encoder classes saved to {le_classes_path}")
    print("\n🎉 Model trained successfully! You can now run the GUI.")

if __name__ == '__main__':
    main()
