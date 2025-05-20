# AgriSmart Application 

## 🌾 Project Overview/Purpose of the Application

AgriSmart empowers farmers by bringing the latest in agriculture technology to their fingertips. It helps in making better decisions regarding crop selection, soil management, disease prediction, and market trends. With simple tools, AI recommendations, and real-time data, AgriSmart ensures increased productivity and reduced risks.

Farmers are no longer left behind. With AgriSmart, they're moving ahead—smarter, stronger, and more sustainable.

<!-- Project Banner Image -->
<p align="center">
  <img src="Screenshot%202025-05-20%20103508.png" alt="AgriSmart Project Banner" width="800"/>
</p><br>
<p align="center">
   <img src="Screenshot%202025-05-20%20103523.png" alt="AgriSmart Project Banner" width="800"/>
</p>

## Why AgriSmart?

Farming is challenging, especially with unpredictable weather, soil conditions, and market fluctuations. AgriSmart supports farmers by integrating advanced technologies like machine learning and data analytics to:

- Recommend the best crops suited for their land and climate.
- Analyze soil fertility to optimize nutrient management.
- Detect crop diseases early to reduce loss.
- Provide up-to-date market rates to maximize profit.
- Deliver the latest agricultural news for informed decisions.

## Key Features & Services
1.**Crop Recommendation**
   Using machine learning algorithms, we analyze soil data, weather conditions, and historical crop performance to recommend the most suitable crops for a 
   specific location.

2.**Soil Fertility Range Analysis**
   Evaluate soil health parameters like pH, nitrogen, phosphorus, and potassium levels to suggest appropriate fertilization strategies.

3.**Crop Disease Detection**
   Upload images of plants and get instant diagnosis of common crop diseases with recommended treatments to save your crops from damage.

4.**Market Rate Updates**
   Real-time updates on crop prices from various markets help farmers decide the best time to sell their produce.

5.**Agricultural News**
   Stay informed with the latest news, trends, and government policies affecting agriculture.

6. **Seed Purchasing Contacts**  
   Access verified seed suppliers and their contact details to ensure quality inputs.
7. **User Authentication**  
   Secure login and registration system for personalized experience and data security.

---

## 🌱 Crop Recommendation — Features and Model Selection

### Input Features

- **N (Nitrogen), P (Phosphorus), K (Potassium):** Essential soil nutrients influencing plant growth.
- **Temperature:** Average ambient temperature affecting crop viability.
- **Humidity:** Atmospheric moisture levels impacting plant health.
- **pH:** Soil acidity or alkalinity, critical for nutrient availability.
- **Rainfall:** Total precipitation supporting crop irrigation.
- **Label:** The target crop type to be recommended.

### Model Evaluation

We tested multiple machine learning models from the `scikit-learn` library:

- Logistic Regression
- Gaussian Naive Bayes
- Support Vector Classifier (SVC)
- K-Nearest Neighbors (KNN)
- Decision Tree Classifier
- Extra Trees Classifier
- Random Forest Classifier
- Bagging Classifier
- Gradient Boosting Classifier
- AdaBoost Classifier

### ✅ Final Model: **Random Forest Classifier**

Random Forest gave the best results in terms of accuracy and generalization, making it the most suitable for recommending crops based on environmental and soil features.

---

## 🌿 Soil Fertility Range Analysis — Features and Model Selection

### Input Features

- **N (Nitrogen)**
- **P (Phosphorus)**
- **K (Potassium)**
- **pH (Soil Acidity)**
- **EC (Electrical Conductivity)**
- **OC (Organic Carbon)**
- **S (Sulphur)**
- **Zn (Zinc)**
- **Fe (Iron)**
- **Cu (Copper)**
- **Mn (Manganese)**
- **B (Boron)**

These features help evaluate soil fertility status and guide farmers in applying the right fertilizers or soil conditioners.

### Model Evaluation

We trained the soil fertility model using the following algorithms:

- Support Vector Classifier (SVC)
- Random Forest Classifier
- Gaussian Naive Bayes
- K-Nearest Neighbors
- Decision Tree Classifier

### ✅ Final Model: **Random Forest Classifier**

After testing multiple classifiers, the **Random Forest Classifier** (non-ensemble) achieved the highest performance in predicting soil fertility classes and was selected as the final model for deployment.

---

## 🛠️ How to Use

- Register or log in to the application.
- Navigate through the services menu:
  - Get crop recommendations based on soil/environment.
  - Check your soil fertility and get nutrient advice.
  - Detect crop diseases via image upload.
  - View current market prices for your crops.
  - Stay updated with agricultural news.
- Access trusted contacts for purchasing seeds.

---

## 📞 Contact Information

For further assistance or partnership inquiries, please contact:

- **Buy Pesticides:** [https://agribegri.com/category/organic-pesticides.php]
- **Buy Fertilizers:**[https://www.indiamart.com/proddetail/fertilizers-15489011355.html]
- **Agriculture Support:**[https://krishijagran.com/contact/#google_vignette]

---

## 🖼️ Visuals

_Add screenshots and images here to showcase:_

- Crop Recommendation Dashboard  
- Soil Fertility Analysis Charts  
- Crop Disease Detection Interface  
- Market Rate Updates  
- Agricultural News Feed  

---

**Thank you for using AgriSmart — empowering farmers for a sustainable future!**
