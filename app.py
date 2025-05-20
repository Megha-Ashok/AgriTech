from flask import Flask, request, render_template
import numpy as np
import pickle

# Load models/scalers
model = pickle.load(open('model.pkl', 'rb'))
sc = pickle.load(open('standscaler.pkl', 'rb'))
ms = pickle.load(open('minmaxscaler.pkl', 'rb'))
fer=pickle.load(open('random_forest_pkl.pkl','rb'))

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/services/recommendation')
def recommendation():
    return render_template('services/recommendation.html')

@app.route('/services/login')
def login():
    return render_template('services/login.html')

@app.route('/services/register')
def register():
    return render_template('services/register.html')

@app.route('/services/soil_fertility_range')
def soil_fertility_range():
    return render_template('services/soil_fertility_range.html')

@app.route('/services/plant_disease')
def plant_disease():
    return render_template('services/plant_disease.html')

@app.route('/services/market-rate')
def market_rate():
    return render_template('services/market-rate.html')

@app.route('/services/agriculture-news')
def agriculture_news():
    return render_template('services/agriculture-news.html')

@app.route("/predict", methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        # 1. Retrieve input values from the form
        N = float(request.form['Nitrogen'])
        P = float(request.form['Phosporus'])  # You may want to correct spelling in your form as well
        K = float(request.form['Potassium'])
        temp = float(request.form['Temperature'])
        humidity = float(request.form['Humidity'])
        ph = float(request.form['Ph'])
        rainfall = float(request.form['Rainfall'])

        # 2. Prepare input features as numpy array
        feature_list = [N, P, K, temp, humidity, ph, rainfall]
        single_pred = np.array(feature_list).reshape(1, -1)

        # 3. Scale features
        scaled_features = ms.transform(single_pred)
        final_features = sc.transform(scaled_features)

        # 4. Predict
        prediction = model.predict(final_features)

        # 5. Map prediction output to crop name
        crop_dict = {
            1: "Rice", 2: "Maize", 3: "Jute", 4: "Cotton", 5: "Coconut", 6: "Papaya", 7: "Orange",
            8: "Apple", 9: "Muskmelon", 10: "Watermelon", 11: "Grapes", 12: "Mango", 13: "Banana",
            14: "Pomegranate", 15: "Lentil", 16: "Blackgram", 17: "Mungbean", 18: "Mothbeans",
            19: "Pigeonpeas", 20: "Kidneybeans", 21: "Chickpea", 22: "Coffee"
        }

        pred_key = prediction[0]
        crop = crop_dict.get(pred_key, None)
        if crop:
            result = f"{crop} is the best crop to be cultivated right there."
        else:
            result = "Sorry, we could not determine the best crop to be cultivated with the provided data."

        # 6. Render the result
        return render_template('services/recommendation.html', result=result)
    else:
        return render_template('services/recommendation.html')
    
@app.route("/predict_fertility", methods=['GET', 'POST'])
def predict_fertility():
    if request.method == 'POST':
        # 1. Get form input
        N = float(request.form['N'])
        P = float(request.form['P'])
        K = float(request.form['K'])
        ph = float(request.form['pH'])
        ec = float(request.form['EC'])   
        organic_carbon = float(request.form['OC']) 
        S = float(request.form['S'])
        Zn = float(request.form['Zn'])
        Fe = float(request.form['Fe'])
        Cu = float(request.form['Cu'])
        Mn = float(request.form['Mn'])
        B = float(request.form['B'])

        # 2. Prepare input
        features = [N, P, K, ph, ec, organic_carbon, S, Zn, Fe, Cu, Mn, B]
        input_array = np.array(features).reshape(1, -1)

        # 3. Predict
        
        prediction = fer.predict(input_array)

        # 4. Map to fertility level
        fertility_level = {
            0: "Low",
            1: "Medium",
            2: "High"
        }
        pred_key = prediction[0]
        level = fertility_level.get(pred_key, "Unknown")

        return render_template('services/soil_fertility_range.html', result=f"The predicted soil fertility level is: {level}")
    else:
        return render_template('services/soil_fertility_range.html')
if __name__ == "__main__":
    app.run(debug=True)
