import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.neighbors import KNeighborsClassifier
import joblib
from sklearn.metrics import classification_report, confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

def main():
    """
    Main function to load data, train a KNN classifier, and evaluate it.
    """
    # 1. Load Data
    try:
        df = pd.read_csv('feature_table.csv')
    except FileNotFoundError:
        print("Error: 'feature_table.csv' not found. Please ensure the feature table exists.")
        return

    # 2. Preprocess Data
    # Separate features (X) and target (y)
    X = df.drop(['ImageName', 'Class'], axis=1)
    y = df['Class']

    # Convert categorical labels to numerical
    # Load the pre-trained label encoder classes for consistency
    le_classes = joblib.load('gui_app/assets/label_encoder.joblib')
    le = LabelEncoder()
    le.fit(le_classes)
    y_encoded = le.transform(y)

    # 3. Feature Scaling
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # 4. Train-Test Split
    # 70% training, 30% testing. random_state for reproducibility.
    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled, y_encoded, test_size=0.3, random_state=42
    )

    # 5. Train Model
    # Using K=3 as a baseline
    knn = KNeighborsClassifier(n_neighbors=3)
    knn.fit(X_train, y_train)

    # 6. Evaluation
    y_pred = knn.predict(X_test)

    # Print classification report
    print("--- Classification Report ---")
    # Use target_names to show 'Day'/'Night' instead of 0/1
    print(classification_report(y_test, y_pred, target_names=le.classes_))

    # Generate and save confusion matrix
    cm = confusion_matrix(y_test, y_pred)
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                xticklabels=le.classes_, yticklabels=le.classes_)
    plt.xlabel('Predicted')
    plt.ylabel('Actual')
    plt.title('Confusion Matrix')
    
    # Save the plot
    output_path = 'confusion_matrix.png'
    plt.savefig(output_path)
    print(f"\nConfusion matrix saved to '{output_path}'")

if __name__ == '__main__':
    main()
