"use client";
import { useState } from "react";

export default function Home() {
  const [form, setForm] = useState({
    age: "",
    sex: "male",
    bmi: "",
    children: "",
    smoker: "no",
    region: "northeast",
  });
  const [prediction, setPrediction] = useState<number | null>(null);
  const [trainingLoss, setTrainingLoss] = useState<number | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    setForm({ ...form, [e.target.name]: e.target.value });
    setPrediction(null);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    try {
      const response = await fetch("http://localhost:5001/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(form),
      });
      const data = await response.json();
      setPrediction(data.predicted_charges);
      setTrainingLoss(data.training_loss)
    } catch (error) {
      console.error("Prediction failed:", error);
      alert("Something went wrong. Please try again.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex flex-col justify-center items-center bg-gradient-to-br from-gray-100 to-blue-100 p-8">
      <h1 className="text-4xl font-bold text-blue-700 mb-2">
        Linear Regression Model for Insurance Charge Prediction
      </h1>
      <p className="text-center text-gray-600 mb-10 max-w-xl">
        AI-powered prediction model that estimates insurance charges based on demographic and health factors
      </p>

      <div className="w-full max-w-4xl grid grid-cols-1 md:grid-cols-2 gap-8">
        {/* Form */}
        <div className="bg-white shadow-lg rounded-xl p-6 space-y-4 border-2 border-black">
          <form onSubmit={handleSubmit} className="space-y-4">
            {[
              { label: "Age", name: "age", type: "number", placeholder: "Enter age" },
              { label: "BMI", name: "bmi", type: "number", placeholder: "Enter BMI" },
              { label: "Children", name: "children", type: "number", placeholder: "Number of children" },
            ].map((field) => (
              <div key={field.name}>
                <label className="block text-base font-semibold text-gray-600 mb-1">{field.label}</label>
                <input
                  name={field.name}
                  type={field.type}
                  value={(form as any)[field.name]}
                  onChange={handleChange}
                  placeholder={field.placeholder}
                  className="w-full border-2 border-black rounded px-3 py-2 focus:outline-none focus:border-black placeholder:text-gray-600 placeholder:italic text-gray-600"
                  required
                />
              </div>
            ))}

            {[
              { label: "Sex", name: "sex", options: ["male", "female"] },
              { label: "Smoker", name: "smoker", options: ["yes", "no"] },
              { label: "Region", name: "region", options: ["northeast", "northwest", "southeast", "southwest"] },
            ].map((select) => (
              <div key={select.name}>
                <label className="block text-base font-semibold text-gray-600 mb-1">{select.label}</label>
                <select
                  name={select.name}
                  value={(form as any)[select.name]}
                  onChange={handleChange}
                  className="w-full border-2 border-black rounded px-3 py-2 focus:outline-none focus:border-black text-gray-600"
                  required
                >
                  {select.options.map((option) => (
                    <option key={option} value={option}>{option.charAt(0).toUpperCase() + option.slice(1)}</option>
                  ))}
                </select>
              </div>
            ))}

            <button
              type="submit"
              className="w-full bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-700 transition font-semibold"
            >
              {isLoading ? "Calculating..." : "Predict Charges"}
            </button>
          </form>
        </div>

        {/* Results */}
        <div className="bg-white shadow-lg rounded-xl p-6 space-y-4 border-2 border-black">
          <h2 className="text-xl font-semibold text-gray-800">Prediction Results</h2>
          {prediction !== null ? (
            <>
              <div className="text-center border-2 border-black rounded-lg p-4">
                <h3 className="text-gray-600">Estimated Annual Charges</h3>
                <p className="text-3xl font-bold text-blue-700">${prediction}</p>
                {form.smoker === "yes" && (
                  <p className="text-sm text-red-600 mt-2">
                    High Risk: Smoking status significantly increases charges
                  </p>
                )}
              </div>
              <div className="text-sm text-gray-600 space-y-1">
                {[
                  { label: "Age", value: form.age },
                  { label: "BMI", value: form.bmi },
                  { label: "Children", value: form.children },
                  { label: "Smoker", value: form.smoker === "yes" ? "Yes" : "No" },
                  { label: "Sex", value: form.sex.charAt(0).toUpperCase() + form.sex.slice(1) },
                  { label: "Region", value: form.region.charAt(0).toUpperCase() + form.region.slice(1) },
                ].map((item) => (
                  <p key={item.label}><strong>{item.label}:</strong> {item.value}</p>
                ))}
              </div>
              {/* === NEW SECTION: model loss summary === */}
              {trainingLoss !== null && (
                <div className="pt-4 mt-4 border-t border-gray-300 text-gray-700 text-sm">
                  <p>
                    <strong>Model training RMSE:</strong> ${trainingLoss}
                  </p>
                  <p className="italic">
                    On average, the model’s predictions differ from the actual charges in the training data
                    by about <strong>${trainingLoss}</strong>. A lower RMSE indicates a more accurate model.
                  </p>
                </div>
              )}
            </>
          ) : (
            <p className="text-gray-500 text-center py-10">
              Fill in the form and click "Predict Charges" to see the result.
            </p>
          )}
        </div>
      </div>
    </div>
  );
}