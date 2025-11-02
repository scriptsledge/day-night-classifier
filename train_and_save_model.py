
import pandas as pd
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.neighbors import KNeighborsClassifier
import joblib
import os

def main():
    """
    Trains the model on the full dataset and saves the scaler and model.
    """
    # 1. Load Data
    try:
        df = pd.read_csv('feature_table.csv')
    except FileNotFoundError:
        print("Error: '02_Feature_Table.csv' not found.")
        return

    # 2. Preprocess Data
    X = df.drop(['ImageName', 'Class'], axis=1)
    y = df['Class']

    le = LabelEncoder()
    y_encoded = le.fit_transform(y)

    # 3. Feature Scaling
    # Important: Fit the scaler on the ENTIRE dataset
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # 4. Train Model
    # Train on the ENTIRE dataset
    knn = KNeighborsClassifier(n_neighbors=3)
    knn.fit(X_scaled, y_encoded)

    # 5. Save the scaler and model
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

if __name__ == '__main__':
    main()
