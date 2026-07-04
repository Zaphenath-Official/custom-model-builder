from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import numpy as np
import pandas as pd
import os
import io
import secrets
import urllib.request
import datetime
from datetime import timezone
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor  # <-- Added for async job dispatching

# Secure cryptographic password hashing libraries
from werkzeug.security import generate_password_hash, check_password_hash

from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OrdinalEncoder, StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split

# Core AutoML Advanced Tournament Models Ecosystem
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from lightgbm import LGBMRegressor, LGBMClassifier
from xgboost import XGBRegressor, XGBClassifier
from catboost import CatBoostRegressor, CatBoostClassifier

from services.supabase_service import SupabaseService
from adapters.storage import SupabaseStorageAdapter

load_dotenv()

app = Flask(__name__)
CORS(app)

MODEL_PATH = 'models/automl_winning_engine.joblib'
os.makedirs('models', exist_ok=True)

# Bootstrap the external system layers cleanly
supabase_glob = SupabaseService()
storage_adapter = SupabaseStorageAdapter(supabase_glob)

# Initialize a Background Worker Thread Pool with capacity limit
executor = ThreadPoolExecutor(max_workers=2)

# Thread-safe in-memory cancellation registration matrix
cancelled_jobs = set()

def send_smtp_email(to_email, subject, html_content):
    """Core SMTP utility engine for dispatching secure transactional mail vectors."""
    smtp_user = os.environ.get("SMTP_EMAIL")
    smtp_pass = os.environ.get("SMTP_PASSWORD")
    
    if not smtp_user or not smtp_pass:
        print("⚠️ [SMTP ERROR] Missing SMTP_EMAIL or SMTP_PASSWORD variables.")
        return False

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = f"AutoML Engine <{smtp_user}>"
    msg["To"] = to_email
    msg.attach(MIMEText(html_content, "html"))
    
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(smtp_user, smtp_pass)
        server.sendmail(smtp_user, to_email, msg.as_string())
        server.quit()
        return True
    except Exception as e:
        print(f"❌ [SMTP FAULT] Delivery failed: {str(e)}")
        return False


def send_custom_welcome_email(user_email):
    html = f"""
    <html>
    <body style="font-family: Arial, sans-serif; padding: 20px; background-color: #f4f7f6;">
        <div style="max-width: 600px; background: white; padding: 30px; border-radius: 8px; margin: 0 auto; border-top: 4px solid #00D26A;">
            <h2>🚀 Welcome to AutoML Proto Engine!</h2>
            <p>Your custom account setup is complete. You have bypassed provider free-tier thresholds and are ready to deploy tournament pipelines.</p>
            <p>Log in using the terminal dashboard or connect directly via the React interface layer.</p>
        </div>
    </body>
    </html>
    """
    return send_smtp_email(user_email, "🎯 Account Verified: Welcome to AutoML Engine Arena", html)


def send_otp_reset_email(user_email, otp_code):
    html = f"""
    <html>
    <body style="font-family: Arial, sans-serif; padding: 20px; background-color: #f4f7f6;">
        <div style="max-width: 600px; background: white; padding: 30px; border-radius: 8px; margin: 0 auto; border-top: 4px solid #3b82f6;">
            <h2>🔐 Password Recovery Request</h2>
            <p>We received a request to reset your AutoML Engine account security credentials.</p>
            <p>Use the 6-digit One-Time Password (OTP) validation key below to complete the cycle. This token code expires in 15 minutes.</p>
            <div style="font-size: 32px; font-weight: bold; letter-spacing: 5px; text-align: center; padding: 20px; margin: 20px 0; background: #eff6ff; color: #1d4ed8; border-radius: 6px;">
                {otp_code}
            </div>
            <p>If you did not issue this verification sequence, you can safely ignore this automated message.</p>
        </div>
    </body>
    </html>
    """
    return send_smtp_email(user_email, "🔑 Security Verification: Your One-Time Password (OTP)", html)


def require_app_auth(f):
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return jsonify({"error": "Unauthorized. Missing token context."}), 401
        
        token = auth_header.split(" ")[1]
        session_query = supabase_glob.client.table("app_sessions").select("*").eq("token", token).execute()
        
        if not session_query.data:
            return jsonify({"error": "Session expired or invalid. Access denied."}), 401
            
        request.user_id = session_query.data[0]["user_id"]
        request.token = token
        return f(*args, **kwargs)
    wrapper.__name__ = f.__name__
    return wrapper


@app.route('/auth/register', methods=['POST'])
def register():
    data = request.get_json() or {}
    email = data.get('email', '').strip().lower()
    password = data.get('password', '')
    
    if not email or not password:
        return jsonify({"error": "Email and password fields are required parameters."}), 400
        
    try:
        existing = supabase_glob.client.table("app_users").select("id").eq("email", email).execute()
        if existing.data:
            return jsonify({"error": "User with this email profile is already registered."}), 400
            
        password_hash = generate_password_hash(password)
        user_record = supabase_glob.client.table("app_users").insert({
            "email": email,
            "password_hash": password_hash
        }).execute().data[0]
        
        send_custom_welcome_email(email)
        
        return jsonify({"message": "User registered successfully!", "user_id": user_record["id"]}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route('/auth/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    email = data.get('email', '').strip().lower()
    password = data.get('password', '')
    
    try:
        user_query = supabase_glob.client.table("app_users").select("*").eq("email", email).execute()
        if not user_query.data:
            return jsonify({"error": "Invalid credential pair parameters."}), 401
            
        user = user_query.data[0]
        if not check_password_hash(user["password_hash"], password):
            return jsonify({"error": "Invalid credential pair parameters."}), 401
            
        session_token = f"sess_{secrets.token_hex(24)}"
        supabase_glob.client.table("app_sessions").insert({
            "user_id": user["id"],
            "token": session_token
        }).execute()
        
        return jsonify({
            "message": "Login successful!",
            "access_token": session_token,
            "user_id": user["id"]
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route('/auth/forgot-password', methods=['POST'])
def forgot_password():
    data = request.get_json() or {}
    email = data.get('email', '').strip().lower()
    
    if not email:
        return jsonify({"error": "Target account email parameter is required."}), 400
        
    try:
        user_check = supabase_glob.client.table("app_users").select("id").eq("email", email).execute()
        if not user_check.data:
            return jsonify({"message": "If the account profile exists, an OTP validation sequence has been triggered."}), 200
            
        otp_code = "".join([str(secrets.randbelow(10)) for _ in range(6)])
        expiration = (datetime.datetime.now(timezone.utc) + datetime.timedelta(minutes=15)).isoformat()
        
        supabase_glob.client.table("app_otps").delete().eq("email", email).execute()
        
        supabase_glob.client.table("app_otps").insert({
            "email": email,
            "otp_code": otp_code,
            "expires_at": expiration
        }).execute()
        
        send_otp_reset_email(email, otp_code)
        
        return jsonify({"message": "If the account profile exists, an OTP validation sequence has been triggered."}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/auth/reset-password-otp', methods=['POST'])
def reset_password_otp():
    data = request.get_json() or {}
    email = data.get('email', '').strip().lower()
    otp_code = data.get('otp', '').strip()
    new_password = data.get('new_password', '')
    
    if not email or not otp_code or not new_password:
        return jsonify({"error": "Missing essential verification parameters."}), 400
        
    try:
        otp_query = supabase_glob.client.table("app_otps").select("*").eq("email", email).eq("otp_code", otp_code).execute()
        if not otp_query.data:
            return jsonify({"error": "Invalid validation code token matching sequence failed."}), 400
            
        record = otp_query.data[0]
        expires_at = datetime.datetime.fromisoformat(record["expires_at"].replace("Z", "+00:00"))
        
        if datetime.datetime.now(timezone.utc) > expires_at:
            supabase_glob.client.table("app_otps").delete().eq("email", email).execute()
            return jsonify({"error": "The validation credentials token has expired."}), 400
            
        new_hash = generate_password_hash(new_password)
        supabase_glob.client.table("app_users").update({"password_hash": new_hash}).eq("email", email).execute()
        
        supabase_glob.client.table("app_otps").delete().eq("email", email).execute()
        
        user_data = supabase_glob.client.table("app_users").select("id").eq("email", email).execute().data[0]
        supabase_glob.client.table("app_sessions").delete().eq("user_id", user_data["id"]).execute()
        
        return jsonify({"message": "Password updated successfully across all platform nodes!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/auth/me', methods=['GET'])
@require_app_auth
def get_profile_details():
    try:
        user_query = supabase_glob.client.table("app_users").select("id", "email", "created_at").eq("id", request.user_id).execute()
        if not user_query.data:
            return jsonify({"error": "Profile data records not found."}), 404
        return jsonify({"user": user_query.data[0]}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/auth/logout', methods=['POST'])
@require_app_auth
def logout():
    try:
        supabase_glob.client.table("app_sessions").delete().eq("token", request.token).execute()
        return jsonify({"message": "Successfully logged out across all engine gateways."}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


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


def async_training_worker(job_id, file_bytes, targets, features, model_name, user_id):
    """Asynchronous pipeline execution running decoupled inside a thread cluster worker pool."""
    try:
        if job_id in cancelled_jobs:
            return

        # Step 1: Update status to running
        supabase_glob.client.table("training_jobs").update({"status": "running", "progress": 15}).eq("id", job_id).execute()
        
        df = pd.read_csv(io.BytesIO(file_bytes))
        df = df.dropna(subset=targets)
        
        if job_id in cancelled_jobs:
            raise Exception("Job execution terminated by user signal request.")

        supabase_glob.client.table("training_jobs").update({"progress": 30}).eq("id", job_id).execute()
        X, y, numerical_features, categorical_features = auto_profile_and_split_v2(df, targets, features)

        if isinstance(y, pd.DataFrame):
            if y.shape[1] == 1:
                y = y.iloc[:, 0]
            else:
                raise Exception("Multi-output prediction is unsupported by this engine setup.")

        target_encoder = None
        if not pd.api.types.is_numeric_dtype(y):
            target_encoder = LabelEncoder()
            y = target_encoder.fit_transform(y.astype(str))
            is_regression = False  
        else:
            is_regression = True if y.nunique() > 20 else False

        if job_id in cancelled_jobs:
            raise Exception("Job execution terminated by user signal request.")

        supabase_glob.client.table("training_jobs").update({"progress": 50}).eq("id", job_id).execute()
        
        # Unique local execution buffer to isolate parallel file processing states
        thread_isolated_path = f"models/engine_{job_id}.joblib"
        production_package, _ = execute_automl_tournament(
            X, y, numerical_features, categorical_features, is_regression, target_encoder, thread_isolated_path, job_id
        )
        
        if job_id in cancelled_jobs:
            raise Exception("Job execution terminated by user signal request.")

        supabase_glob.client.table("training_jobs").update({"progress": 80}).eq("id", job_id).execute()
        
        existing_named_models = supabase_glob.client.table("models_registry") \
            .select("model_version") \
            .eq("user_id", user_id) \
            .eq("model_name", model_name) \
            .execute()
            
        next_version = max([row["model_version"] for row in existing_named_models.data]) + 1 if existing_named_models.data else 1
        versioned_filename = f"{model_name.replace(' ', '_')}_v{next_version}"
        
        buffer = io.BytesIO()
        joblib.dump(production_package, buffer)
        cloud_url = storage_adapter.upload_model_file(user_id, versioned_filename, buffer)
        
        payload = {
            "user_id": user_id,
            "model_name": model_name,
            "model_version": next_version,
            "problem_type": production_package['problem_type'],
            "algorithm_name": production_package['algorithm_name'],
            "performance_score": float(production_package['performance_score']),
            "features": production_package['features'],
            "targets": targets,
            "storage_url": cloud_url,
            "api_key": f"sk_engine_{secrets.token_hex(16)}",
            "has_been_downloaded": False
        }
        
        supabase_glob.client.table("models_registry").insert(payload).execute()
        
        # Complete the operation lifecycle updates
        supabase_glob.client.table("training_jobs").update({
            "status": "completed", 
            "progress": 100,
            "completed_at": datetime.datetime.now(timezone.utc).isoformat()
        }).eq("id", job_id).execute()
        
        # Cleanup isolated working cache
        if os.path.exists(thread_isolated_path):
            os.remove(thread_isolated_path)
            
    except Exception as e:
        # Determine if failure was via user cancellation signal to preserve structured message columns
        error_msg = "Pipeline processing halted successfully: Terminated by user request." if job_id in cancelled_jobs else str(e)
        
        supabase_glob.client.table("training_jobs").update({
            "status": "failed", 
            "error_message": error_msg
        }).eq("id", job_id).execute()
        
        # Clean cache up on cancellation fault
        thread_isolated_path = f"models/engine_{job_id}.joblib"
        if os.path.exists(thread_isolated_path):
            os.remove(thread_isolated_path)
    finally:
        if job_id in cancelled_jobs:
            cancelled_jobs.remove(job_id)


@app.route('/targets-features-train', methods=['POST'])
def get_targets_features_and_train():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
        
    file = request.files['file']
    targets = request.form.getlist('targets')
    features = request.form.getlist('features')
    model_name = request.form.get('model_name', 'unnamed_model')
    user_id = request.form.get('user_id')
    
    if not user_id:
        return jsonify({"error": "Missing user_id parameter"}), 400

    # Read binary stream instantly before closing request boundary Context
    file_bytes = file.read()
    
    try:
        # Initialize job entry inside tracking database
        job_record = supabase_glob.client.table("training_jobs").insert({
            "user_id": user_id,
            "model_name": model_name,
            "status": "pending",
            "progress": 0
        }).execute().data[0]
        
        # Dispatch to Background Thread Worker instantly
        executor.submit(
            async_training_worker, 
            job_record["id"], file_bytes, targets, features, model_name, user_id
        )
        
        return jsonify({
            "message": "Model training pipeline queued successfully!",
            "job_id": job_record["id"],
            "status": "pending"
        }), 202
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/developer/active-jobs', methods=['GET'])
def get_active_jobs():
    """Retrieve all pending or running jobs for a specific user to power real-time polling sync."""
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({"error": "Missing user_id parameter context"}), 400
    try:
        res = supabase_glob.client.table("training_jobs") \
            .select("*") \
            .eq("user_id", user_id) \
            .in_("status", ["pending", "running"]) \
            .execute()
            
        active_list = []
        for job in res.data:
            active_list.append({
                "id": job["id"],
                "label": job.get("model_name", "unnamed_model"),
                "status": job["status"]
            })
        return jsonify({"active_jobs": active_list}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/targets-features-cancel', methods=['POST'])
def cancel_training_operation():
    """Register absolute process termination signal parameters and break running pipelines."""
    data = request.get_json() or {}
    job_id = data.get('job_id')
    user_id = data.get('user_id')
    
    if not job_id:
        return jsonify({"error": "Missing job_id parameter payload marker"}), 400
        
    try:
        # Intercept background thread lifecycle processing maps instantly
        cancelled_jobs.add(job_id)
        
        # Propagate immediate execution change state downstream inside database layer
        supabase_glob.client.table("training_jobs").update({
            "status": "failed",
            "error_message": "Pipeline processing halted successfully: Terminated by user request."
        }).eq("id", job_id).execute()
        
        return jsonify({"status": "terminated", "message": "Pipeline processing halted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/developer/jobs/<user_id>', methods=['GET'])
def get_user_jobs(user_id):
    """Retrieve tracking list for interface fallback pooling."""
    try:
        res = supabase_glob.client.table("training_jobs").select("*").eq("user_id", user_id).order("started_at", desc=True).execute()
        return jsonify({"jobs": res.data}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/developer/models', methods=['GET'])
def list_models():
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({"error": "Missing user_id context parameters"}), 400
    res = supabase_glob.client.table("models_registry").select("*").eq("user_id", user_id).execute()
    return jsonify({"models": res.data}), 200


@app.route('/v1/predict', methods=['POST'])
def public_api_predict():
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return jsonify({"error": "Unauthorized. Missing or malformed access token."}), 401
    
    api_key = auth_header.split(" ")[1]
    model_meta = supabase_glob.verify_api_key(api_key)
    
    if not model_meta:
        return jsonify({"error": "Forbidden. Provided API Token key is invalid."}), 403
        
    data = request.get_json()
    
    try:
        with urllib.request.urlopen(model_meta["storage_url"]) as response:
            model_bytes = io.BytesIO(response.read())
            package = joblib.load(model_bytes)
            
        pipeline = package['pipeline']
        expected_features = package['features']
        input_data = {feat: [data.get(feat)] for feat in expected_features}
        input_df = pd.DataFrame(input_data)
        
        for col in expected_features:
            if col in package.get('numerical_features', []):
                input_df[col] = pd.to_numeric(input_df[col], errors='coerce')
            elif col in package.get('categorical_features', []):
                input_df[col] = input_df[col].astype(object).fillna('missing_data')
        
        prediction = pipeline.predict(input_df)
        
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
        return jsonify({"error": "No trained model found."}), 400

    package = joblib.load(MODEL_PATH)
    pipeline = package['pipeline']
    expected_features = package['features']
    data = request.get_json() or {}

    try:
        input_data = {feat: [data.get(feat)] for feat in expected_features}
        input_df = pd.DataFrame(input_data)

        for col in expected_features:
            if col in package.get('numerical_features', []):
                input_df[col] = pd.to_numeric(input_df[col], errors='coerce')
            elif col in package.get('categorical_features', []):
                input_df[col] = input_df[col].astype(object).fillna('missing_data')

        prediction = pipeline.predict(input_df)
        
        if package.get('target_encoder') is not None:
            predicted_value = str(package['target_encoder'].inverse_transform(prediction)[0])
        else:
            predicted_value = round(float(prediction[0]), 2)

        return jsonify({"status": "success", "problem_type": package['problem_type'], "prediction": predicted_value})
    except Exception as e:
        return jsonify({"error": f"Inference pipeline execution failed: {str(e)}"}), 500


@app.route('/developer/models/download/<model_id>', methods=['GET'])
def download_model_binary(model_id):
    model_query = supabase_glob.client.table("models_registry").select("*").eq("id", model_id).execute()
    if len(model_query.data) == 0:
        return jsonify({"error": "Model artifact profile not found."}), 404
        
    model_data = model_query.data[0]
    
    try:
        with urllib.request.urlopen(model_data["storage_url"]) as response:
            file_bytes = response.read()
            
        supabase_glob.client.table("models_registry").update({"has_been_downloaded": True}).eq("id", model_id).execute()
        clean_filename = f"{model_data['model_name'].replace(' ', '_')}_v{model_data['model_version']}.joblib"
        
        return io.BytesIO(file_bytes), 200, {
            'Content-Type': 'application/octet-stream',
            'Content-Disposition': f'attachment; filename={clean_filename}'
        }
    except Exception as e:
        return jsonify({"error": str(e)}), 500


def auto_profile_and_split_v2(df, target_columns, core_features):
    keep_columns = core_features + target_columns
    df = df[keep_columns].copy()
    
    X = df.drop(columns=target_columns)
    y = df[target_columns]
    
    numerical_features = []
    categorical_features = []
    X.columns = X.columns.str.strip()
    
    for col in X.columns:
        non_null_samples = X[col].dropna()
        if non_null_samples.empty:
            categorical_features.append(col)
            X[col] = X[col].astype(str)
            continue
            
        try:
            pd.to_numeric(non_null_samples)
            is_numeric = True
        except (ValueError, TypeError):
            is_numeric = False
            
        if is_numeric and X[col].nunique() > 10:
            numerical_features.append(col)
        else:
            categorical_features.append(col)
            X[col] = X[col].astype(str)
            
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
    return ColumnTransformer(transformers=[('num', num_transformer, num_cols), ('cat', cat_transformer, cat_cols)])


def execute_automl_tournament(X, y, num_cols, cat_cols, is_regression=True, target_encoder=None, specific_path=MODEL_PATH, job_id=None):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    preprocessor = build_preprocessing_pipeline(num_cols, cat_cols)
    
    if is_regression:
        models = {
            'RandomForest': RandomForestRegressor(n_estimators=50, max_depth=12, random_state=42),
            'LightGBM': LGBMRegressor(n_estimators=100, learning_rate=0.05, random_state=42, verbose=-1),
            'XGBoost': XGBRegressor(n_estimators=100, max_depth=6, learning_rate=0.05, random_state=42),
            'CatBoost': CatBoostRegressor(iterations=150, learning_rate=0.05, depth=6, random_state=42, verbose=0)
        }
    else:
        models = {
            'RandomForest': RandomForestClassifier(n_estimators=50, max_depth=12, random_state=42),
            'LightGBM': LGBMClassifier(n_estimators=100, learning_rate=0.05, random_state=42, verbose=-1),
            'XGBoost': XGBClassifier(n_estimators=100, max_depth=6, learning_rate=0.05, random_state=42, eval_metric='logloss'),
            'CatBoost': CatBoostClassifier(iterations=150, learning_rate=0.05, depth=6, random_state=42, verbose=0)
        }
        
    best_score, best_pipeline, winning_algorithm = -float('inf'), None, "Unknown"
    
    for name, model in models.items():
        # Intercept iteration steps during high volume data computations instantly if cancellation signal triggers
        if job_id and job_id in cancelled_jobs:
            raise Exception("Job execution terminated by user signal request.")

        full_pipeline = Pipeline(steps=[('preprocessor', preprocessor), ('estimator', model)])
        full_pipeline.fit(X_train, y_train)
        score = full_pipeline.score(X_test, y_test)
        
        if score > best_score:
            best_score, best_pipeline, winning_algorithm = score, full_pipeline, name
            
    production_package = {
        'pipeline': best_pipeline,
        'features': list(X.columns),
        'numerical_features': num_cols,
        'categorical_features': cat_cols,
        'problem_type': 'regression' if is_regression else 'classification',
        'algorithm_name': winning_algorithm,
        'performance_score': best_score,
        'target_encoder': target_encoder  
    }
    
    joblib.dump(production_package, specific_path)
    return production_package, specific_path


if __name__ == '__main__':
    app.run(debug=True)