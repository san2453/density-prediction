from flask import Flask, render_template, request
import pandas as pd
from sklearn.utils.validation import joblib
import numpy as np
app = Flask(__name__)
model = joblib.load('./density_prediction.pkl')
features = model.feature_names_in_
data = {key: None for key in features}
df = pd.DataFrame(data, index=[0])
@app.route('/')
def index():
    material = 1
    scan_speed = 0
    hatch_distance = 0
    laser_power = 0
    layer_thickness = 0
    return render_template('index.html', 
        material = material, 
        scan_speed = scan_speed, 
        hatch_distance = hatch_distance, 
        laser_power = laser_power, 
        layer_thickness = layer_thickness,
        prediction = False
        )

@app.route('/predict', methods=['POST'])
def predict():
    material = int(request.form['material'])
    scan_speed = float(request.form['scan_speed'])
    hatch_distance = float(request.form['hatch_distance'])
    laser_power = float(request.form['laser_power'])
    layer_thickness = float(request.form['layer_thickness'])
    energy_density=round(laser_power/(hatch_distance*scan_speed*layer_thickness),2)

    maximum={'max scan speed': 2000.0,'max laser power': 370.0,'max energy density': 1166.04}
    minimum={'min scan speed': 18.76,'min laser power': 70.0,'min energy density': 24.6}


    data = {'Material': [material], 'Scan Speed (mm/s)': [scan_speed],
            'Hatch Distance (mm)': [hatch_distance],'Laser Power (Watts)': [laser_power],
            'Layer thickness(mm)': [layer_thickness],'Energy density (joule/mm^3)': [energy_density]}

    # Create a DataFrame from the input data
    df = pd.DataFrame(data)
    print(type(maximum))
    print(type(minimum))

    # Normalize the features
 
    df['Scan Speed (mm/s)'] = (df['Scan Speed (mm/s)'] - minimum.get("min scan speed", 0)) / (maximum.get("max scan speed", 1) - minimum.get("min scan speed", 0))
    df['Laser Power (Watts)'] = (df['Laser Power (Watts)'] - minimum.get("min laser power", 0)) / (maximum.get("max laser power", 1) - minimum.get("min laser power", 0))
    df['Energy density (joule/mm^3)'] = (df['Energy density (joule/mm^3)'] - minimum.get("min energy density", 0)) / (maximum.get("max energy density", 1) - minimum.get("min energy density", 0))
    

    # You can process the input data here
    alloyDensity = np.round(model.predict(df), decimals=3)
    
    
    
    return render_template('index.html', 
        material = material, 
        scan_speed = scan_speed, 
        hatch_distance = hatch_distance, 
        laser_power = laser_power, 
        layer_thickness = layer_thickness,
        prediction = True,
        alloyDensity = alloyDensity[0]
        )
    

if __name__ == '__main__':
    app.run()
