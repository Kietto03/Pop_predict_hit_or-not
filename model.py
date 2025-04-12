import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler, LabelEncoder
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
import xgboost as xgb
import pickle

# 1. Load Dataset
df = pd.read_csv("output_dataset.csv")
print(f"Dataset shape: {df.shape}")
print("Columns:", df.columns.tolist())

# 2. Feature selection (exclude file name & label)
X = df.drop(columns=['file_name', 'label'])
y = df['label']

# 3. Encode labels
label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)

# 4. Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=3)

# 5. Normalize features
scaler = MinMaxScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# 6. Train models
models = {
    "svm": SVC(kernel='linear'),
    "knn": KNeighborsClassifier(n_neighbors=5),
    "logreg": LogisticRegression(max_iter=10000),
    "xgbc": xgb.XGBClassifier(use_label_encoder=False, eval_metric='mlogloss')
}

for name, model in models.items():
    print(f"Training {name}...")
    model.fit(X_train_scaled, y_train)
    with open(f"{name}_model.pkl", 'wb') as f:
        pickle.dump(model, f)

# 7. Save scaler and label encoder
with open("scaler.pkl", "wb") as f:
    pickle.dump(scaler, f)

with open("label_encoder.pkl", "wb") as f:
    pickle.dump(label_encoder, f)

print("\n✅ All models and preprocessing tools saved successfully!")
