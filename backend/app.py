from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import os

app = Flask(__name__)
CORS(app, origins="*")  # Allow all origins for simplicity

# Load dataset
data_url = 'https://raw.githubusercontent.com/JovianML/opendatasets/master/data/medical-charges.csv'
df = pd.read_csv(data_url)

# Encode binary categorical columns
df['sex'] = df['sex'].map({'male': 1, 'female': 0})
df['smoker'] = df['smoker'].map({'yes': 1, 'no': 0})

# One-hot encode 'region'
df_encoded = pd.get_dummies(df, columns=['region'], drop_first=False, dtype=int)

# Separate features and target
inputs = df_encoded.drop('charges', axis=1)
target = df_encoded['charges']

# Train-test split
input_train, input_test, target_train, target_test = train_test_split(
    inputs, target, test_size=0.2, random_state=42
)

# Train the model
model = LinearRegression().fit(input_train, target_train)

# RMSE function
def rmse(y_true, y_pred):
    return np.sqrt(np.mean((y_true - y_pred) ** 2))

# Evaluate
training_loss = rmse(target_train, model.predict(input_train))
test_loss = rmse(target_test, model.predict(input_test))

# Store input structure
input_columns = input_train.columns.tolist()

@app.route("/predict", methods=["POST"])
def predict():
    try:
        input_data = request.json
        input_df = pd.DataFrame([input_data])
        input_df['sex'] = input_df['sex'].map({'male': 1, 'female': 0})
        input_df['smoker'] = input_df['smoker'].map({'yes': 1, 'no': 0})
        input_encoded = pd.get_dummies(input_df, columns=['region'], dtype=int)
        input_encoded = input_encoded.reindex(columns=input_columns, fill_value=0)

        prediction = model.predict(input_encoded)[0]

        return jsonify({
            "predicted_charges": round(prediction, 2),
            "training_loss": round(training_loss, 2),
            "test_loss": round(test_loss, 2)
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    print("Starting Flask server...")
    port = int(os.environ.get("PORT", 5001))  # Use PORT from env if available
    app.run(host="0.0.0.0", port=port)