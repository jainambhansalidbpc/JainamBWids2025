import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report
import joblib

# 1. Load Data
try:
    # Ensure this matches your actual filename
    df = pd.read_csv('first_order_df.csv') 
except FileNotFoundError:
    try:
        df = pd.read_csv('transaction_dataset.csv')
    except:
        print("Error: Dataset not found. Please download it.")
        exit()

# 2. Select Features (The Fix)
# We strictly select ONLY the columns we know exist in your file
features_to_use = ['Value', 'BlockHeight', 'TimeStamp']
target_column = 'isError'

try:
    X = df[features_to_use]
    y = df[target_column]
except KeyError as e:
    print(f"Error: Missing column {e} in your CSV. Check your file.")
    exit()

# 3. Preprocessing
imputer = SimpleImputer(strategy='mean')
X_imputed = imputer.fit_transform(X)

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_imputed)

# 4. Training
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

print("Training Model...")
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# 5. Evaluate
predictions = model.predict(X_test)
print("Model Accuracy Report:")
print(classification_report(y_test, predictions))

# 6. Save
joblib.dump(model, 'fraud_model.pkl')
joblib.dump(scaler, 'scaler.pkl')
joblib.dump(imputer, 'imputer.pkl')
print("Model and processors saved successfully.")
