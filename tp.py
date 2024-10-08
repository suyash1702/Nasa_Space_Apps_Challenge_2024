import pandas as pd
import os

# List files in the current directory
print("Files in the current directory:")
print(os.listdir('.'))

# Try to load the CSV file
try:
    soil_moisture_data = pd.read_csv('soil_moisture1.csv')
    print("Soil Moisture Data:")
    print(soil_moisture_data.head())

    # Extract latitude and longitude
    latitudes = soil_moisture_data['latitude'].unique()
    longitudes = soil_moisture_data['longitude'].unique()

    # Display the unique latitude and longitude values
    print("\nUnique Latitude Values:")
    print(latitudes)

    print("\nUnique Longitude Values:")
    print(longitudes)

except FileNotFoundError:
    print("Error: The file 'soil_moisture1.csv' was not found. Please check the file path and try again.")
except Exception as e:
    print(f"An error occurred: {e}")
