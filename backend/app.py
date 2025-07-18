from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

app = Flask(__name__)
CORS(app, origins="http://localhost:3000")

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

# Train the model
model = LinearRegression().fit(inputs, target)

def rmse(targets, predictions):
    return np.sqrt(np.mean(np.square(targets-predictions)))

training_predictions = model.predict(inputs)
training_loss = rmse(target, training_predictions)

# Save input columns for later use
input_columns = inputs.columns.tolist()


@app.route("/predict", methods=["POST"])
def predict():
    try:
        input_data = request.json

        # Convert input to DataFrame
        input_df = pd.DataFrame([input_data])
        input_df['sex'] = input_df['sex'].map({'male': 1, 'female': 0})
        input_df['smoker'] = input_df['smoker'].map({'yes': 1, 'no': 0})
        input_encoded = pd.get_dummies(input_df, columns=['region'], dtype=int)

        # Reindex to match training columns
        input_encoded = input_encoded.reindex(columns=input_columns, fill_value=0)

        # Predict
        prediction = model.predict(input_encoded)[0]

        return jsonify({"predicted_charges": round(prediction, 2),
                        "training_loss": round(training_loss, 2)})

    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    print("Starting Flask server...")
    app.run(debug=True, port=5001)