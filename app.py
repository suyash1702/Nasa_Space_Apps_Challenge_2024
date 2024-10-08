from flask import Flask, render_template, request, redirect, url_for
import pandas as pd



app = Flask(__name__, template_folder='templates')


# Define your routes and functions below


def check_irrigation_need(current_soil_moisture, optimal_soil_moisture, root_zone_depth, moisture_holding_capacity):
    # Calculate the moisture deficit and determine if irrigation is needed.
    moisture_deficit = optimal_soil_moisture - current_soil_moisture
    irrigation_needed = moisture_deficit * root_zone_depth * moisture_holding_capacity

    if irrigation_needed > 0:
        return f"Irrigation is needed. Apply approximately {irrigation_needed:.2f} mm of water."
    else:
        return "No irrigation is needed at this time."

def perform_soil_moisture_analysis(crop_name, soil_type, latitude, longitude, crop_age):
    # Load crop data
    crop_data = pd.read_csv('crop_data.csv')
    print("Loaded crop data:", crop_data)  # Debugging print statement

    # Filter crop data for the specific crop and soil type
    matching_crop = crop_data[
        (crop_data['Crop Name'].str.strip().str.lower() == crop_name.lower()) &
        (crop_data['Soil Type'].str.strip().str.lower() == soil_type.lower())
    ]
    print("Matching crop data:", matching_crop)  # Debugging print statement

    # Check if matching crop data is found
    if matching_crop.empty:
        return f"Error: No matching crop data found for crop '{crop_name}' and soil type '{soil_type}'."

    # Extract the required parameters for the specified crop and growth phase
    crop_info = matching_crop.iloc[0]
    optimal_soil_moisture = crop_info['Optimal Soil Moisture Content (cm³/cm³)']
    moisture_holding_capacity = crop_info['Moisture Holding Capacity (mm)']

    # Load soil moisture data (assuming soil_moisture1.csv has 'soil_moisture' column)
    soil_moisture_data = pd.read_csv('soil_moisture1.csv')
    current_soil_moisture = soil_moisture_data['soil_moisture'].mean()  # Calculate average soil moisture

    root_zone_depth = 30  # in cm

    # Determine if irrigation is needed
    result_message = check_irrigation_need(
        current_soil_moisture=current_soil_moisture,
        optimal_soil_moisture=optimal_soil_moisture,
        root_zone_depth=root_zone_depth,
        moisture_holding_capacity=moisture_holding_capacity
    )

    return result_message

# Route for the homepage
@app.route('/')
def index():
    return render_template('index.html')  # Renders the homepage

# Route to handle form submission and perform analysis
@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        # Get form data
        latitude = float(request.form.get('latitude'))  # Convert to float
        longitude = float(request.form.get('longitude'))  # Convert to float
        crop_name = request.form.get('crop_name').strip()
        crop_age = int(request.form.get('crop_age'))  # Convert to int
        soil_type = request.form.get('soil_type').strip()

        # Debugging prints
        print(f"Latitude: {latitude}, Longitude: {longitude}, Crop Name: {crop_name}, Crop Age: {crop_age}, Soil Type: {soil_type}")

        # Perform soil moisture analysis
        result = perform_soil_moisture_analysis(crop_name, soil_type, latitude, longitude, crop_age)

        # Debugging print
        print(f"Analysis Result: {result}")

        # Redirect to the result page with the analysis result
        return redirect(url_for('result', result=result))

    except ValueError:
        print("Error: Please ensure latitude, longitude, and crop age are entered correctly as numeric values.")
        return render_template('result.html', message="Error: Please ensure latitude, longitude, and crop age are entered correctly as numeric values.")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
        return render_template('result.html', message=f"An unexpected error occurred: {str(e)}")


@app.route('/result')
def result():
    result = request.args.get('result', '')
    return render_template('result.html', message=result)

# Main entry point
if __name__ == '__main__':
    app.run(debug=True)
