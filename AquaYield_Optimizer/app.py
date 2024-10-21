from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
from data_analysis import perform_soil_moisture_analysis
from testapi import predict_diseases_with_symptoms

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/soil-analysis')
def soil_analysis():
    return render_template('soil-analysis.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        # Get form data
        crop_name = request.form['crop_name']
        soil_type = request.form['soil_type']
        latitude = float(request.form['latitude'])
        longitude = float(request.form['longitude'])
        crop_age = request.form['crop_age']

        # Convert crop_age to integer if it's a number
        try:
            crop_age_int = int(crop_age)
        except ValueError:
            crop_age_int = 0  # Default to 0 if conversion fails

        # Perform soil moisture analysis
        result = perform_soil_moisture_analysis(crop_name, soil_type, latitude, longitude, crop_age_int)

        # Check for errors in the result
        if 'Error' in result:
            return render_template('result.html', error_message=result['Error'])

        # Get disease predictions
        disease_predictions = predict_diseases_with_symptoms(crop_name, crop_age_int, result.get('Growth Phase', 'Unknown'), soil_type)

        # Generate additional info
        additional_info = "Based on the analysis, consider adjusting irrigation schedules and monitoring for early signs of plant stress."

        return render_template('result.html', 
                               result=result,
                               disease_predictions=disease_predictions,
                               additional_info=additional_info)

    except Exception as e:
        error_message = f"An unexpected error occurred: {str(e)}"
        return render_template('result.html', error_message=error_message)

@app.route('/analysis')
def analysis():
    return render_template('analysis.html')

# Add these new routes
@app.route('/information')
def information():
    return render_template('information.html')

@app.route('/references')
def references():
    return render_template('references.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/result', methods=['POST'])
def result():
    # Get form data
    crop_name = request.form['crop_name']
    soil_type = request.form['soil_type']
    latitude = float(request.form['latitude'])
    longitude = float(request.form['longitude'])
    crop_age = int(request.form['crop_age'])

    # Perform soil moisture analysis
    result = perform_soil_moisture_analysis(crop_name, soil_type, latitude, longitude, crop_age)

    # Get disease predictions
    disease_predictions = predict_diseases_with_symptoms(crop_name, crop_age, result.get('Growth Phase', 'Unknown'), soil_type)

    # Generate additional info (you might want to customize this based on your needs)
    additional_info = "Based on the analysis, consider adjusting irrigation schedules and monitoring for early signs of plant stress. Regular soil testing is recommended to maintain optimal growing conditions."

    return render_template('result.html', 
                           result=result,
                           disease_predictions=disease_predictions,
                           additional_info=additional_info)

@app.route('/sample-data')
def sample_data():
    # Read soil moisture data
    soil_moisture_df = pd.read_csv('soil_moisture2.csv')
    
    # Read crop data
    crop_data_df = pd.read_csv('crop_data.csv')
    
    # Convert DataFrames to HTML tables
    soil_moisture_table = soil_moisture_df.to_html(classes='data-table', index=False)
    crop_data_table = crop_data_df.to_html(classes='data-table', index=False)
    
    return render_template('sample_data.html', 
                           soil_moisture_table=soil_moisture_table,
                           crop_data_table=crop_data_table)

if __name__ == '__main__':
    app.run(debug=True)
