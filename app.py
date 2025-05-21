from flask import Flask, request, render_template,redirect, flash, session,jsonify
import numpy as np
import pickle
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from flask import abort, redirect, url_for
import secrets
from flask_cors import CORS
from pymongo import MongoClient
from datetime import datetime
import requests
from apscheduler.schedulers.background import BackgroundScheduler

# Load models/scalers
model = pickle.load(open('model.pkl', 'rb'))
sc = pickle.load(open('standscaler.pkl', 'rb'))
ms = pickle.load(open('minmaxscaler.pkl', 'rb'))
fer=pickle.load(open('random_forest_pkl.pkl','rb'))

app = Flask(__name__)

app.secret_key =secrets.token_hex(16)

@app.before_request
def require_login():
    open_routes = ['home', 'login', 'register', 'register_details', 'login_details', 'static']
    if request.endpoint not in open_routes and 'user' not in session:
        return render_template('services/login.html')

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

@app.route('/services/market_rate')
def market_rate():
    return render_template('services/market_rate.html')

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

def init_db():
    conn = sqlite3.connect('database.db')
    cur  = conn.cursor()

# 1. Add the is_admin column if it doesn't already exist
    try:
        cur.execute("""
        ALTER TABLE users
        ADD COLUMN is_admin INTEGER NOT NULL DEFAULT 0;
        """)
        print("Added is_admin column.")
    except sqlite3.OperationalError:
    # Will raise OperationalError if the column already exists
       print("is_admin column already exists, skipping ALTER.")

# 2. Promote your chosen email to admin
    admin_email = 'megha@1234'
    cur.execute("""
    UPDATE users
    SET is_admin = 1
    WHERE email = ?
    """, (admin_email,))
    conn.commit()
    print(f"Rows updated (admin promoted): {conn.total_changes}")

# 3. Verify the change
    cur.execute("SELECT name, email, is_admin FROM users WHERE email = ?", (admin_email,))
    row = cur.fetchone()
    print("Verification:", row)

    conn.close()

init_db()

@app.route('/register_details', methods=['GET', 'POST'])
def register_details():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])

        conn = sqlite3.connect('database.db')
        cur = conn.cursor()
        try:
            cur.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)", (name, email, password))
            conn.commit()
            flash("Registration successful! Please log in.", "success")
            return render_template("services/login.html")
        except sqlite3.IntegrityError:
            flash("Account already exists with this email.", "error")
        conn.close()
    return render_template('services/register.html')

@app.route('/login_details', methods=['POST'])
def login_details():
    email = request.form['email']
    password = request.form['password']

    conn = sqlite3.connect('database.db')
    cur  = conn.cursor()
    cur.execute("SELECT name, password, is_admin FROM users WHERE email = ?", (email,))
    row = cur.fetchone()
    conn.close()

    if row and check_password_hash(row[1], password):
        session['user']       = row[0]        # username
        session['user_email'] = email         # email
        session['is_admin']   = bool(row[2])  # True/False
        flash("Login successful!", "success")
        return render_template('home.html')
    else:
        flash("Invalid email or password.", "error")
        return render_template('services/login.html')



def admin_required(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        if not session.get('user'):
            return redirect(url_for('login'))
        if not session.get('is_admin', False):
            abort(403)   # Forbidden
        return f(*args, **kwargs)
    return wrapped

@app.route('/admin/users')
@admin_required
def admin_users():
    conn = sqlite3.connect('database.db')
    cur  = conn.cursor()
    cur.execute("SELECT name, email, password FROM users")
    users = cur.fetchall()
    conn.close()
    return render_template('services/admin_users.html', users=users)
from flask import session, redirect, url_for, flash

@app.route('/logout')
def logout():
    session.clear()
    return render_template('home.html')


CORS(app)

client = MongoClient("mongodb://localhost:27017/")
db = client["market_rates"]
collection = db["crop_rates"]

# Replace this with your real external API endpoint
EXTERNAL_API_URL = EXTERNAL_API_URL = "https://api.data.gov.in/resource/35985678-0d79-46b4-9ed6-6f13308a1d24?api-key=579b464db66ec23bdd000001cdd3946e44ce4aad7209ff7b23ac571b&format=json&filters%5BState%5D=Karnataka&filters%5BDistrict%5D=Dharwad"


def fetch_real_market_rates():
    try:
        # Mock data
        data = {
            "prices": [
                {"crop": "Wheat", "market": "Delhi", "price_per_kg": "25.00"},
                {"crop": "Rice", "market": "Mysore", "price_per_kg": "30.00"}
            ]
        }

        updated_data = []
        for item in data["prices"]:
            updated_data.append({
                "crop_name": item["crop"],
                "location": item["market"],
                "rate_per_kg": float(item["price_per_kg"]),
                "date": datetime.now().strftime("%Y-%m-%d %H:%M")
            })

        collection.delete_many({})
        collection.insert_many(updated_data)
        print(f"Mock database updated at {datetime.now()}")

    except Exception as e:
        print(f"Failed to fetch/update market rates: {e}")
# Scheduler to run fetch every minute
scheduler = BackgroundScheduler()
scheduler.add_job(fetch_real_market_rates, 'interval', minutes=1)
scheduler.start()

@app.route("/api/rates", methods=["GET"])
def get_rates():
    crop = request.args.get("crop")
    if not crop:
        return "Crop is required", 400
    rates = list(collection.find({"crop_name": {"$regex": crop, "$options": "i"}}, {"_id": 0}))
    return jsonify(rates)


if __name__ == '__main__':
    fetch_real_market_rates()  # Initial data fetch on start
    app.run(debug=True)

