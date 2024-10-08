import pandas as pd

# Load the crop data and soil moisture data
crop_data = pd.read_csv('crop_data.csv')
soil_data = pd.read_csv('soil_moisture1.csv')

# Clean up column names in crop_data (optional, depending on your CSV formatting)
crop_data.columns = crop_data.columns.str.strip()

# Define function to perform analysis based on user input
def perform_soil_moisture_analysis(crop_name, soil_type, latitude, longitude, crop_age):
    # Filter the crop data based on user input
    crop_info = crop_data[(crop_data['Crop Name'] == crop_name) & (crop_data['Soil Type'] == soil_type)]

    # Determine the growth phase based on crop age
    crop_phase = None
    phase_duration_sum = 0
    required_irrigation = None
    for _, row in crop_info.iterrows():
        phase_duration_sum += row['Duration of Phase (days)']
        if crop_age <= phase_duration_sum:
            crop_phase = row['Growth Phase']
            required_moisture = row['Optimal Soil Moisture Content (cm³/cm³)']
            required_irrigation = row['Required Irrigation (mm/day)']
            break

    if not crop_phase:
        return f"Crop age {crop_age} exceeds known phases for {crop_name}. Please verify."

    # Find the soil moisture data for the specified coordinates
    soil_info = soil_data[(soil_data['latitude'] == latitude) & (soil_data['longitude'] == longitude)]

    if soil_info.empty:
        return f"No soil moisture data available for coordinates ({latitude}, {longitude})."

    # Calculate the average soil moisture and compare with crop requirements
    avg_soil_moisture = soil_info['adjusted_soil_moisture'].mean()

    # Determine if irrigation is required and how much
    irrigation_needed = "Yes" if avg_soil_moisture < required_moisture else "No"
    irrigation_amount = (required_moisture - avg_soil_moisture) * 1000 if irrigation_needed == "Yes" else 0  # Convert to mm

    # Return the analysis result
    return {
        'Crop Name': crop_name,
        'Soil Type': soil_type,
        'Growth Phase': crop_phase,
        'Average Soil Moisture': avg_soil_moisture,
        'Required Moisture': required_moisture,
        'Irrigation Needed': irrigation_needed,
        'Irrigation Amount (mm/day)': irrigation_amount
    }

# Save this analysis function as a module for the Flask app to use
