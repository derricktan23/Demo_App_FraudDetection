from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, PlainTextResponse
import joblib
import numpy as np
from pydantic import BaseModel

app = FastAPI(
    title="Credit Card Fraud Detection API",
    description="""An API that utilizes a Machine Learning model to detect fraudulent credit card transactions.""",
    version="1.0.0", debug=True)

try:
    # Load the model; ensure this is the correct version of scikit-learn
    model = joblib.load('credit_card_fraud.pkl')
except Exception as e:
    raise HTTPException(status_code=500, detail=f"Model loading error: {str(e)}")

@app.get("/", response_class=PlainTextResponse)
async def running():
    note = """
Credit Card Fraud Detection API 🙌🏻

Note: add "/docs" to the URL to get the Swagger UI Docs or "/redoc"
    """
    return note

favicon_path = 'favicon.png'
@app.get('/favicon.png', include_in_schema=False)
async def favicon():
    return FileResponse(favicon_path)

class FraudDetection(BaseModel):
    amt: float
    age: float
    distance_km: float

@app.post('/predict')
def predict(data: FraudDetection):
    # The model expects 28 features in a specific order.
    # We will take the 3 features from the user and pad the rest with constant values.
    # Based on the dataset, the other features are one-hot encoded booleans.
    # We will assume a default value of False (or 0) for these features.

    # The order of features must be:
    # ['amt', 'age', 'distance_km', 'category_food_dining', 'category_gas_transport', 
    #  'category_grocery_net', 'category_grocery_pos', 'category_health_fitness', 
    #  'category_home', 'category_kids_pets', 'category_misc_net', 'category_misc_pos', 
    #  'category_personal_care', 'category_shopping_net', 'category_shopping_pos', 
    #  'category_travel', 'state_bin_Top 3', 'Month_name_Aug', 'Month_name_Dec', 
    #  'Month_name_Feb', 'Month_name_Jan', 'Month_name_Jul', 'Month_name_Jun', 
    #  'Month_name_Mar', 'Month_name_May', 'Month_name_Nov', 'Month_name_Oct', 'Month_name_Sep']
    
    # Create the full list of features with a constant value of False (0) for the rest
    features = [
        data.amt,
        data.age,
        data.distance_km,
        False,  # category_food_dining
        False,  # category_gas_transport
        False,  # category_grocery_net
        False,  # category_grocery_pos
        False,  # category_health_fitness
        False,  # category_home
        False,  # category_kids_pets
        False,  # category_misc_net
        False,  # category_misc_pos
        False,  # category_personal_care
        False,  # category_shopping_net
        False,  # category_shopping_pos
        False,  # category_travel
        False,  # state_bin_Top_3
        False,  # Month_name_Aug
        False,  # Month_name_Dec
        False,  # Month_name_Feb
        False,  # Month_name_Jan
        False,  # Month_name_Jul
        False,  # Month_name_Jun
        False,  # Month_name_Mar
        False,  # Month_name_May
        False,  # Month_name_Nov
        False,  # Month_name_Oct
        False   # Month_name_Sep
    ]

    features_array = np.array([features])
    
    try:
        predictions = model.predict(features_array)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")

    return {"prediction": "fraudulent" if predictions[0] == 1 else "not fraudulent"}