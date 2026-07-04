from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import numpy as np
import pandas as pd
import os
import io

from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OrdinalEncoder, StandardScaler, LabelEncoder
from lightgbm import LGBMRegressor, LGBMClassifier
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.model_selection import train_test_split

from services.supabase_service import SupabaseService
from adapters.storage import SupabaseStorageAdapter
import secrets

from dotenv import load_dotenv
import urllib.request

load_dotenv()

app = Flask(__name__)
CORS(app)

MODEL_PATH = 'models/automl_winning_engine.joblib'

# Ensure the local models directory exists to prevent FileNotFoundError
os.makedirs('models', exist_ok=True)

# Bootstrap the external infrastructure layer cleanly
supabase_glob = SupabaseService()
storage_adapter = SupabaseStorageAdapter(supabase_glob)


@app.route('/auth/register', methods=['POST'])
def register():
    data = request.get_json()
    try:
        res = supabase_glob.register_user(data['email'], data['password'])
        return jsonify({"message": "User registered successfully!", "user_id": res.user.id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route('/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    try:
        res = supabase_glob.login_user(data['email'], data['password'])
        return jsonify({
            "message": "Login successful!",
            "access_token": res.session.access_token,
            "user_id": res.user.id
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route('/inspect-csv', methods=['POST'])
def inspect_csv():
    if 'file' not in request.files:
        return jsonify({"error": "No file payload provided"}), 400
    file = request.files['file']
    df_preview = pd.read_csv(file, nrows=5)
    return jsonify({
        "columns": list(df_preview.columns),
        "preview": df_preview.head(2).to_dict(orient='records')
    })


@app.route('/targets-features-train', methods=['POST'])
def get_targets_features_and_train():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
        
    file = request.files['file']
    targets = request.form.getlist('targets')
    features = request.form.getlist('features')
    model_name = request.form.get('model_name', 'unnamed_model')
    user_id = request.form.get('user_id')
    
    df = pd.read_csv(file)
    
    # Clean the Target Column before processing
    df = df.dropna(subset=targets)
    
    # 1. Split the data using your profiler
    X, y, numerical_features, categorical_features = auto_profile_and_split_v2(df, targets, features)

    # Flatten y from a 2D DataFrame into a 1D Series if a single target was passed
    if isinstance(y, pd.DataFrame):
        if y.shape[1] == 1:
            y = y.iloc[:, 0]
        else:
            return jsonify({"error": "Multi-output prediction is not supported yet by this AutoML engine."}), 400

    # 🚨 TARGET STRING CONVERSION SECURITY GUARDRAIL:
    target_encoder = None
    if not pd.api.types.is_numeric_dtype(y):
        print("🔤 [TARGET DETECTED AS STRING] Initializing Target LabelEncoder Processing Pipeline...")
        target_encoder = LabelEncoder()
        y = target_encoder.fit_transform(y.astype(str))
        is_regression = False  # Text labels are strictly categorical classification metrics
    else:
        if y.nunique() > 20:
            is_regression = True
        else:
            is_regression = False

    print(f"data: 🚀 [AUTO-DETECT] Inferred problem type. Is Regression: {is_regression}")
    
    # Pass the target_encoder explicitly to be wrapped inside the joblib dictionary structure
    production_package, _ = execute_automl_tournament(
        X, y, numerical_features, categorical_features, is_regression, target_encoder
    )
    
    # Fetch all models with this exact name for this specific user to calculate versioning
    existing_named_models = supabase_glob.client.table("models_registry") \
        .select("model_version") \
        .eq("user_id", user_id) \
        .eq("model_name", model_name) \
        .execute()
        
    if len(existing_named_models.data) > 0:
        versions = [row["model_version"] for row in existing_named_models.data]
        next_version = max(versions) + 1
    else:
        next_version = 1

    versioned_filename = f"{model_name.replace(' ', '_')}_v{next_version}"
    
    buffer = io.BytesIO()
    joblib.dump(production_package, buffer)
    
    cloud_url = storage_adapter.upload_model_file(user_id, versioned_filename, buffer)
    
    payload = {
        "user_id": user_id,
        "model_name": model_name,
        "model_version": next_version,
        "problem_type": production_package['problem_type'],
        "performance_score": float(production_package['performance_score']),
        "storage_url": cloud_url,
        "api_key": f"sk_engine_{secrets.token_hex(16)}",
        "has_been_downloaded": False
    }
    
    record = supabase_glob.client.table("models_registry").insert(payload).execute().data[0]
    
    return jsonify({
        "message": "Model trained and recorded globally!",
        "model_id": record["id"],
        "api_key": record["api_key"],
        "download_url": record["storage_url"]
    }), 200


@app.route('/developer/models', methods=['GET'])
def list_models():
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({"error": "Missing user_id context string parameters"}), 400
    models = supabase_glob.get_user_models(user_id)
    return jsonify({"models": models}), 200


@app.route('/v1/predict', methods=['POST'])
def public_api_predict():
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return jsonify({"error": "Unauthorized. Missing or malformed access token."}), 401
    
    api_key = auth_header.split(" ")[1]
    model_meta = supabase_glob.verify_api_key(api_key)
    
    if not model_meta:
        return jsonify({"error": "Forbidden. Provided API Token key is invalid or suspended."}), 403
        
    data = request.get_json()
    
    try:
        with urllib.request.urlopen(model_meta["storage_url"]) as response:
            model_bytes = io.BytesIO(response.read())
            package = joblib.load(model_bytes)
            
        pipeline = package['pipeline']
        expected_features = package['features']
        
        # Construct structural validation runtime parameters dataframe
        input_data = {feat: [data.get(feat)] for feat in expected_features}
        input_df = pd.DataFrame(input_data)
        
        # FORCE CASTING AT THE PANDAS LEVEL DURING INFERENCE
        for col in expected_features:
            if col in package.get('numerical_features', []):
                input_df[col] = pd.to_numeric(input_df[col], errors='coerce')
            elif col in package.get('categorical_features', []):
                input_df[col] = input_df[col].astype(object).fillna('missing_data')
        
        # Execute calculations safely
        prediction = pipeline.predict(input_df)
        
        # Dynamic decoding mapping structure
        if package.get('target_encoder') is not None:
            predicted_value = str(package['target_encoder'].inverse_transform(prediction)[0])
        else:
            predicted_value = round(float(prediction[0]), 4)
        
        return jsonify({
            "status": "success",
            "model_name": model_meta["model_name"],
            "prediction": predicted_value
        }), 200
        
    except Exception as e:
        return jsonify({"error": f"API Gateway Runtime inference fault: {str(e)}"}), 500


@app.route('/predict', methods=['POST'])
def predict():
    if not os.path.exists(MODEL_PATH):
        return jsonify({"error": "No trained model found. Train a model first using /targets-features-train"}), 400

    package = joblib.load(MODEL_PATH)
    pipeline = package['pipeline']
    expected_features = package['features']

    data = request.get_json()
    if not data:
        return jsonify({"error": "Missing JSON request body"}), 400

    try:
        # Restructure input dictionary into a single-row Pandas DataFrame matching expected features
        input_data = {feat: [data.get(feat)] for feat in expected_features}
        input_df = pd.DataFrame(input_data)

        # FORCE CASTING AT THE PANDAS LEVEL DURING INFERENCE
        for col in expected_features:
            if col in package.get('numerical_features', []):
                input_df[col] = pd.to_numeric(input_df[col], errors='coerce')
            elif col in package.get('categorical_features', []):
                input_df[col] = input_df[col].astype(object).fillna('missing_data')

        # Fire data through the pipeline
        prediction = pipeline.predict(input_df)
        
        # Dynamic decoding mapping structure
        if package.get('target_encoder') is not None:
            predicted_value = str(package['target_encoder'].inverse_transform(prediction)[0])
        else:
            predicted_value = round(float(prediction[0]), 2)

        return jsonify({
            "status": "success",
            "problem_type": package['problem_type'],
            "prediction": predicted_value
        })
    except Exception as e:
        return jsonify({"error": f"Inference pipeline execution failed: {str(e)}"}), 500


@app.route('/developer/models/download/<model_id>', methods=['GET'])
def download_model_binary(model_id):
    model_query = supabase_glob.client.table("models_registry").select("*").eq("id", model_id).execute()
    if len(model_query.data) == 0:
        return jsonify({"error": "Model artifact target profile not found"}), 404
        
    model_data = model_query.data[0]
    
    try:
        with urllib.request.urlopen(model_data["storage_url"]) as response:
            file_bytes = response.read()
            
        supabase_glob.client.table("models_registry") \
            .update({"has_been_downloaded": True}) \
            .eq("id", model_id) \
            .execute()
            
        clean_filename = f"{model_data['model_name'].replace(' ', '_')}_v{model_data['model_version']}.joblib"
        
        return io.BytesIO(file_bytes), 200, {
            'Content-Type': 'application/octet-stream',
            'Content-Disposition': f'attachment; filename={clean_filename}'
        }
    except Exception as e:
        return jsonify({"error": f"Failed to package file stream transfer output: {str(e)}"}), 500


def auto_profile_and_split_v2(df, target_columns, core_features):
    """
    Upgraded, bulletproof profiler. Explicitly isolates numerical and 
    categorical blocks by checking real sample values rather than loose object types.
    """
    keep_columns = core_features + target_columns
    df = df[keep_columns].copy()
    
    X = df.drop(columns=target_columns)
    y = df[target_columns]
    
    numerical_features = []
    categorical_features = []
    
    # Clean up column spaces or weird string patterns from form inputs
    X.columns = X.columns.str.strip()
    
    for col in X.columns:
        # Drop NaNs temporarily just to inspect the true content of the column
        non_null_samples = X[col].dropna()
        
        if non_null_samples.empty:
            categorical_features.append(col)
            X[col] = X[col].astype(str)
            continue
            
        # Check if the underlying values are truly numbers
        try:
            pd.to_numeric(non_null_samples)
            is_numeric = True
        except (ValueError, TypeError):
            is_numeric = False
            
        # Sort into buckets based on true data content
        if is_numeric and X[col].nunique() > 10:
            numerical_features.append(col)
        else:
            categorical_features.append(col)
            X[col] = X[col].astype(str)
            
    print("\n=======================================================")
    print(f"📊 [PROFILER ARCHITECTURE VERIFICATION]")
    print(f"   🔢 NUMERICAL FEATURES   : {numerical_features}")
    print(f"   🔤 CATEGORICAL FEATURES : {categorical_features}")
    print("=======================================================\n")
    
    return X, y, numerical_features, categorical_features


def build_preprocessing_pipeline(num_cols, cat_cols):
    num_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())
    ])
    
    cat_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='constant', fill_value='missing_data')),
        ('encoder', OrdinalEncoder(handle_unknown='use_encoded_value', unknown_value=-1))
    ])
    
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', num_transformer, num_cols),
            ('cat', cat_transformer, cat_cols)
        ]
    )
    return preprocessor


def execute_automl_tournament(X, y, num_cols, cat_cols, is_regression=True, target_encoder=None):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    preprocessor = build_preprocessing_pipeline(num_cols, cat_cols)
    
    if is_regression:
        models = {
            'RandomForest': RandomForestRegressor(n_estimators=50, max_depth=12, random_state=42),
            'LightGBM': LGBMRegressor(n_estimators=100, learning_rate=0.05, random_state=42)
        }
    else:
        models = {
            'RandomForest': RandomForestClassifier(n_estimators=50, max_depth=12, random_state=42),
            'LightGBM': LGBMClassifier(n_estimators=100, learning_rate=0.05, random_state=42)
        }
        
    best_score = -float('inf')
    best_pipeline = None
    
    for name, model in models.items():
        full_pipeline = Pipeline(steps=[('preprocessor', preprocessor), ('estimator', model)])
        full_pipeline.fit(X_train, y_train)
        score = full_pipeline.score(X_test, y_test)
        
        if score > best_score:
            best_score = score
            best_pipeline = full_pipeline
            
    production_package = {
        'pipeline': best_pipeline,
        'features': list(X.columns),
        'numerical_features': num_cols,
        'categorical_features': cat_cols,
        'problem_type': 'regression' if is_regression else 'classification',
        'performance_score': best_score,
        'target_encoder': target_encoder  # Package the LabelEncoder safely
    }
    
    joblib.dump(production_package, MODEL_PATH)
    return production_package, MODEL_PATH


if __name__ == '__main__':
    app.run(debug=True)