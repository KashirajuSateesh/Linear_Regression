# Linear_Regression
# 🧠 Insurance Charges Predictor (Machine Learning Project)

This project is a machine learning-powered web app that predicts **medical insurance charges** based on user inputs like age, BMI, smoking status, number of children, and region. It demonstrates the application of **linear regression** for real-world healthcare-related cost estimation.

**Live Link**: [Insurance Charge Predictor](https://linear-regression-blush.vercel.app/)

## 📊 Problem Statement

Insurance providers estimate individual charges based on multiple demographic and health-related factors. This project builds a regression model to predict these charges using a publicly available dataset.

---

## 🔍 Dataset

- 📄 **Source**: [Medical Cost Personal Dataset](https://www.kaggle.com/mirichoi0218/insurance)
- 💡 **Features Used**:
  - Age
  - Sex (encoded)
  - BMI (Body Mass Index)
  - Children (number of dependents)
  - Smoker (binary)
  - Region (one-hot encoded)

---

## 🔧 Tech Stack

| Area        | Tools Used                         |
|-------------|------------------------------------|
| Language    | Python                             |
| Libraries   | Pandas, NumPy, Scikit-learn         |
| Model       | Linear Regression                  |
| API Server  | Flask                              |
| Frontend UI | Next.js + Tailwind CSS (local only) |

---

## 🧪 Model & Training

- Model: `LinearRegression()` from `sklearn`
- Evaluation Metric: **RMSE (Root Mean Squared Error)**
- Preprocessing:
  - One-hot encoding of `region`
  - Mapping of binary categories (`sex`, `smoker`)
  - Optional: Standardization (for numerical features)

---

## 📈 Prediction Output

The model returns:
- Predicted insurance charge (based on input features)
- RMSE loss on training data (to indicate model fit)

Example prediction:
```json
{
  "predicted_charges": 12837.56,
  "training_loss": 6035.21
}
