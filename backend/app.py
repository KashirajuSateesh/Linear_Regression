from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

app = Flask(__name__)
CORS(app, origins="http://localhost:3000")  # Update this if deploying to Vercel

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

# Split into training and test data
input_train, input_test, target_train, target_test = train_test_split(
    inputs, target, test_size=0.2, random_state=42
)

# Train the model on training data
model = LinearRegression().fit(input_train, target_train)

# Define RMSE function
def rmse(y_true, y_pred):
    return np.sqrt(np.mean(np.square(y_true - y_pred)))

# Compute losses
training_predictions = model.predict(input_train)
test_predictions = model.predict(input_test)
training_loss = rmse(target_train, training_predictions)
test_loss = rmse(target_test, test_predictions)

print(training_loss, test_loss)

# Save input column structure for reindexing during prediction
input_columns = input_train.columns.tolist()

@app.route("/predict", methods=["POST"])
def predict():
    try:
        input_data = request.json

        # Convert input to DataFrame
        input_df = pd.DataFrame([input_data])
        input_df['sex'] = input_df['sex'].map({'male': 1, 'female': 0})
        input_df['smoker'] = input_df['smoker'].map({'yes': 1, 'no': 0})
        input_encoded = pd.get_dummies(input_df, columns=['region'], dtype=int)

        # Align input with model's expected columns
        input_encoded = input_encoded.reindex(columns=input_columns, fill_value=0)

        # Make prediction
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
    app.run(debug=True, port=5001)