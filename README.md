# 💜 ChurnCure – Customer Churn Prediction Web App

![Python](https://img.shields.io/badge/Python-3.10-blue) ![Flask](https://img.shields.io/badge/Flask-2.3-green) ![Scikit-learn](https://img.shields.io/badge/Scikit--learn-1.3-orange)

Predict whether a customer will **churn** and get actionable retention insights with **ChurnCure**!

---

## 🚀 Features

* **Predict Churn:** Instantly see if a customer is likely to leave.
* **Churn Probability:** Know the risk as a percentage.
* **Suggested Discount:** Retain high-risk customers with recommended discounts.
* **Color-coded Results:**

  * 🔴 Churn → Red
  * 🟢 No Churn → Green
* **Interactive Frontend:** Easy-to-use web interface.
* **Supports Multiple Services:** Phone, Internet, Streaming TV/Movies, and more.

---

## 🎨 Demo

Form Image:
<img width="629" height="714" alt="image" src="https://github.com/user-attachments/assets/5645cebd-b36b-46e0-8d3f-1ad4dd7a4ca2" />

Result Image:
<img width="369" height="168" alt="image" src="https://github.com/user-attachments/assets/b1c54fbc-4d60-4128-a20d-a54189b9fea5" />


---

## 🛠 Built With

* **Backend:** Python, Flask
* **Machine Learning:** Scikit-learn, Pandas, NumPy, Joblib
* **Frontend:** HTML, CSS, JavaScript
* **Deployment Ready:** Compatible with platforms like Render 

---

## ⚡ How to Run Locally

1. Clone the repo:

```bash
git clone https://github.com/JaweriaAsif745/churn-prediction-web.git
```

2. Navigate to backend and install dependencies:

```bash
cd churn-prediction-web/backend
pip install -r requirements.txt
```

3. Run the Flask app:

```bash
python app.py
```

4. Open in browser:

```
http://127.0.0.1:5000
```

---

## 📝 Notes

* Project **not yet deployed online**.
* Ensure `churn_model.pkl` exists in the `models` folder.
* Currently uses **local Flask server**; environment variables can be added for API keys or secret configs.

---

## 📂 Project Structure

```
backend/  ─ Flask app 
frontend/ ─ HTML, CSS, JS
models/   ─ Trained ML model
reports/  ─ Model evaluation & charts
requirements.txt
```

---

## 🌟 Future Features

* Online **deployment** with cloud service (Render/Heroku).
* **User authentication** to manage multiple predictions.
* Export prediction results to **CSV or PDF**.
* Integrate **email notifications** for high-risk churn customers.

---

## 📞 Contact

* Developer: Jaweria Asif
* GitHub: [JaweriaAsif745](https://github.com/JaweriaAsif745)

---
