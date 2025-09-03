from flask import Flask, request, jsonify
import pandas as pd
import numpy as np
import joblib
from sklearn.preprocessing import StandardScaler, RobustScaler, MinMaxScaler
from flask_cors import CORS
import warnings
warnings.filterwarnings('ignore')
import os

dir = os.getcwd()

app = Flask(__name__)
CORS(app)

# Load the trained model
model = joblib.load(os.path.join(dir, "Doctor_app", 'knn_model.pkl'))

# Initialize scalers (these should match the training preprocessing)
sscaler = StandardScaler()
rscaler = RobustScaler()
mscaler = MinMaxScaler()

import os
dir = os.getcwd()

# Load the original dataset to fit scalers with the same parameters used during training
try:
    original_data = pd.read_csv(os.path.join(dir, "Doctor_app", 'diabetes.csv'))

    # Apply the same preprocessing as in training
    # Group education levels < 3 to 3
    original_data.loc[original_data['Education'] < 3, 'Education'] = 3
    
    # Remove duplicates
    original_data.drop_duplicates(inplace=True)
    original_data.reset_index(drop=True, inplace=True)
    
    # Fit scalers on the original training data (without target variable)
    features_for_scaling = original_data.drop('Diabetes_binary', axis=1)
    
    # Fit the scalers
    sscaler.fit(features_for_scaling)
    rscaler.fit(features_for_scaling)
    mscaler.fit(features_for_scaling)
    
    print("✅ Scalers fitted successfully with original training data")
    
except Exception as e:
    print(f"⚠️ Warning: Could not load original dataset for scaler fitting: {e}")
    print("Using default scalers - predictions may be less accurate")

def preprocess_input(data):
    """
    Preprocess input data exactly as done during training
    """
    try:
        # Create DataFrame from input
        df = pd.DataFrame([data])
        
        # # Apply education grouping rule
        # df.loc[df['Education'] < 3, 'Education'] = 3
        
        # Create a copy for scaling
        df_scaled = df.copy()
        
        # Apply the same scaling as in training
        # StandardScaler for BMI, Age, GenHlth (but we don't have Age in the final model)
        # RobustScaler for MentHlth, PhysHlth (but these are dropped in final model)
        # MinMaxScaler for Education, Income (but these are dropped in final model)
        
        # Since the final model drops these columns: ['MentHlth', 'PhysHlth', 'DiffWalk', 'Sex', 'Age', 'Education', 'Income']
        # We only need to scale the features that are actually used
        
        # Features that are kept in the final model (from analysis of notebook):
        # ['HighBP', 'HighChol', 'CholCheck', 'BMI', 'Smoker', 'Stroke', 'HeartDiseaseorAttack', 
        #  'PhysActivity', 'Fruits', 'Veggies', 'HvyAlcoholConsump', 'AnyHealthcare', 'NoDocbcCost', 'GenHlth']
        
        # Scale BMI and GenHlth with StandardScaler
        if len(sscaler.feature_names_in_ if hasattr(sscaler, 'feature_names_in_') else []) > 0:
            # Create full feature set for scaling
            full_features = pd.DataFrame(0, index=[0], columns=[
                'HighBP', 'HighChol', 'CholCheck', 'BMI', 'Smoker', 'Stroke', 
                'HeartDiseaseorAttack', 'PhysActivity', 'Fruits', 'Veggies', 
                'HvyAlcoholConsump', 'AnyHealthcare', 'NoDocbcCost', 'GenHlth',
                'MentHlth', 'PhysHlth', 'DiffWalk', 'Sex', 'Age', 'Education', 'Income'
            ])
            
            # Fill with actual values
            for col in df.columns:
                if col in full_features.columns:
                    full_features[col] = df[col].values[0]
            
            # Apply scaling
            scaled_features = sscaler.transform(full_features)
            scaled_df = pd.DataFrame(scaled_features, columns=full_features.columns)
            
            # Use scaled values for BMI and GenHlth
            df_scaled['BMI'] = scaled_df['BMI'].values[0]
            df_scaled['GenHlth'] = scaled_df['GenHlth'].values[0]
        
        # Remove the columns that were dropped in training
        columns_to_drop = ['MentHlth', 'PhysHlth', 'DiffWalk', 'Sex', 'Age', 'Education', 'Income']
        for col in columns_to_drop:
            if col in df_scaled.columns:
                df_scaled = df_scaled.drop(columns=[col])
        
        # Ensure the order matches the model's expected features
        expected_features = ['HighBP', 'HighChol', 'CholCheck', 'BMI', 'Smoker', 'Stroke',
                           'HeartDiseaseorAttack', 'PhysActivity', 'Fruits', 'Veggies',
                           'HvyAlcoholConsump', 'AnyHealthcare', 'NoDocbcCost', 'GenHlth']
        
        # Reorder columns
        df_final = df_scaled[expected_features]
        print(df_final.values)
        
        return df_final.values
        
    except Exception as e:
        print(data)
        print(f"Error in preprocessing: {e}")
        # Fallback: return data as-is for basic features
        basic_features = ['HighBP', 'HighChol', 'CholCheck', 'BMI', 'Smoker', 'Stroke',
                         'HeartDiseaseorAttack', 'PhysActivity', 'Fruits', 'Veggies',
                         'HvyAlcoholConsump', 'AnyHealthcare', 'NoDocbcCost', 'GenHlth']
        
        values = []
        for feature in basic_features:
            if feature in data:
                if feature in ['BMI', 'GenHlth'] and feature == 'BMI':
                    # Simple BMI scaling (approximate)
                    values.append((data[feature] - 25) / 5)  # rough standardization
                elif feature == 'GenHlth':
                    # Simple GenHlth scaling
                    values.append((data[feature] - 3) / 1.5)  # rough standardization
                else:
                    values.append(data[feature])
            else:
                values.append(0)
        
        return np.array([values])

@app.route('/predict', methods=['POST'])
def predict():
    """
    Predict diabetes risk based on input features
    """
    try:
        # Get data from request
        data = request.json
        
        # Validate required fields
        required_fields = ['HighBP', 'HighChol', 'CholCheck', 'BMI', 'Smoker', 'Stroke',
                          'HeartDiseaseorAttack', 'PhysActivity', 'Fruits', 'Veggies',
                          'HvyAlcoholConsump', 'AnyHealthcare', 'NoDocbcCost', 'GenHlth']
        
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return jsonify({
                'error': f'Missing required fields: {missing_fields}'
            }), 400
        
        # Preprocess the input data
        processed_data = preprocess_input(data)
        
        # Make prediction
        prediction = model.predict(processed_data)[0]
        
        # Get prediction probability
        probabilities = model.predict_proba(processed_data)[0]
        probability = probabilities[1]  # Probability of diabetes (class 1)
        
        # Prepare response
        result = {
            'prediction': int(prediction),
            'probability': float(probability),
            'risk_level': 'High' if prediction == 1 else 'Low',
            'confidence': float(max(probabilities)),
            'input_data': data,
            'message': 'Prediction completed successfully'
        }
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            'error': f'Prediction failed: {str(e)}',
            'message': 'Please check your input data and try again'
        }), 500

@app.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint
    """
    try:
        # Test model loading
        test_data = {
            'HighBP': 0, 'HighChol': 0, 'CholCheck': 1, 'BMI': 25.0,
            'Smoker': 0, 'Stroke': 0, 'HeartDiseaseorAttack': 0,
            'PhysActivity': 1, 'Fruits': 1, 'Veggies': 1,
            'HvyAlcoholConsump': 0, 'AnyHealthcare': 1, 'NoDocbcCost': 0,
            'GenHlth': 3
        }
        
        processed_data = preprocess_input(test_data)
        test_prediction = model.predict(processed_data)
        
        return jsonify({
            'status': 'healthy',
            'model_loaded': True,
            'test_prediction': int(test_prediction[0]),
            'message': 'Server is running properly',
            'features_expected': 14
        })
        
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'error': str(e),
            'model_loaded': False
        }), 500

@app.route('/model-info', methods=['GET'])
def model_info():
    """
    Get information about the loaded model
    """
    try:
        return jsonify({
            'model_type': 'K-Nearest Neighbors',
            'model_class': str(type(model).__name__),
            'n_neighbors': getattr(model, 'n_neighbors', 'Unknown'),
            'metric': getattr(model, 'metric', 'Unknown'),
            'weights': getattr(model, 'weights', 'Unknown'),
            'features_count': 14,
            'target_classes': ['No Diabetes', 'Diabetes'],
            'preprocessing': {
                'education_grouping': 'Values < 3 grouped to 3',
                'feature_scaling': {
                    'BMI': 'StandardScaler',
                    'GenHlth': 'StandardScaler',
                    'dropped_features': ['MentHlth', 'PhysHlth', 'DiffWalk', 'Sex', 'Age', 'Education', 'Income']
                }
            }
        })
        
    except Exception as e:
        return jsonify({
            'error': f'Could not retrieve model info: {str(e)}'
        }), 500

@app.route('/', methods=['GET'])
def home():
    """
    Home endpoint with API documentation
    """
    return jsonify({
        'service': 'Diabetes Doctor API',
        'version': '1.0.0',
        'description': 'AI-powered diabetes risk assessment using K-Nearest Neighbors',
        'endpoints': {
            '/predict': 'POST - Predict diabetes risk',
            '/health': 'GET - Health check',
            '/model-info': 'GET - Model information',
            '/': 'GET - API documentation'
        },
        'required_features': [
            'HighBP', 'HighChol', 'CholCheck', 'BMI', 'Smoker', 'Stroke',
            'HeartDiseaseorAttack', 'PhysActivity', 'Fruits', 'Veggies',
            'HvyAlcoholConsump', 'AnyHealthcare', 'NoDocbcCost', 'GenHlth'
        ],
        'example_request': {
            'HighBP': 0,
            'HighChol': 0,
            'CholCheck': 1,
            'BMI': 25.0,
            'Smoker': 0,
            'Stroke': 0,
            'HeartDiseaseorAttack': 0,
            'PhysActivity': 1,
            'Fruits': 1,
            'Veggies': 1,
            'HvyAlcoholConsump': 0,
            'AnyHealthcare': 1,
            'NoDocbcCost': 0,
            'GenHlth': 3
        }
    })

if __name__ == '__main__':
    print("🩺 Starting Diabetes Doctor Server...")
    print("🔬 Loading KNN model from knn_model.pkl...")
    
    try:
        # Test model loading
        test_data = np.array([[0, 0, 1, 25.0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 3]])
        test_pred = model.predict(test_data)
        print(f"✅ Model loaded successfully! Test prediction: {test_pred[0]}")
        
    except Exception as e:
        print(f"❌ Error loading model: {e}")
        print("Make sure knn_model.pkl exists in the current directory")
    
    print("🌐 Server will be running on http://localhost:5002")
    print("📊 Endpoints available:")
    print("   - POST /predict - Diabetes risk prediction")
    print("   - GET /health - Health check")
    print("   - GET /model-info - Model information")
    print("   - GET / - API documentation")
    
    # Run the server
    app.run(host='0.0.0.0', port=5002, debug=True)
