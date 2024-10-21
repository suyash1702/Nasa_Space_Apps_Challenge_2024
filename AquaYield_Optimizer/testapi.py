import os
from dotenv import load_dotenv
import google.generativeai as genai
import json

# Load API key from environment variables
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# Configure the Gemini API
genai.configure(api_key=api_key)

# Create the model configuration
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "application/json",
}

# Instantiate the generative model
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
)

# Start a chat session
chat_session = model.start_chat(
    history=[]
)

# Function to predict diseases, symptoms, and prevention methods based on crop parameters
def predict_diseases_with_symptoms(crop_name, crop_age, growth_phase, soil_type):
    # Create a dynamic prompt based on input parameters
    prompt = (f"Predict possible three diseases for {crop_name} at age {crop_age} days "
              f"in the {growth_phase} phase with soil type {soil_type}. "
              f"Also provide symptoms and prevention methods for each disease.")
    
    # Send the prompt to the API
    response = chat_session.send_message(prompt)
    
    # Print the raw response for debugging
    # print("Raw Response from API:", response.text)
    
    try:
        response_text = response.text  # Access the response as plain text
        # Parse the response if it's in JSON format or handle it as plain text
        response_data = json.loads(response_text)
        if 'diseases' in response_data and response_data['diseases']:
            return response_data['diseases']
        else:
            print("No diseases found in the API response")
            return []
    except json.JSONDecodeError:
        print("Error decoding JSON from API response")
        return []
    except Exception as e:
        print(f"Unexpected error in disease prediction: {str(e)}")
        return []

# Example usage
# predict_diseases_with_symptoms(crop_name="Maize", crop_age=15, growth_phase="Seedling", soil_type="Loamy")
