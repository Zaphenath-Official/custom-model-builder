import sys
import requests
import os
import json
import tkinter as tk
from tkinter import filedialog
import getpass

BASE_URL = "http://127.0.0.1:5000"
session_state = {"user_id": None, "token": None}


def main_menu():
    print("\n=== 🚗 CUSTOM AUTOMATED ML PROTO ENGINE CLI ===")
    if session_state["token"]:
        print(f"👉 LOGGED IN AS ID: {session_state['user_id'][:8]}...")
    else:
        print("👉 STATUS: Not Authenticated")
    print("-----------------------------------------------")
    print("1. Create New Account (Register)")
    print("2. Log In to Session")
    print("3. Forgot Password (OTP Verification)")
    print("4. View Account Profile Details")
    print("5. Profile CSV Layout & Train Automated Model Arena")
    print("6. View All My Trained Models & Detailed Specifications")
    print("7. Run Live Prediction on a Trained Model")
    print("8. Global Logout Session Clear")
    print("9. Exit Engine")
    choice = input("Select operation code (1-9): ").strip()
    
    if choice == "1": register()
    elif choice == "2": login()
    elif choice == "3": forgot_password_otp()
    elif choice == "4": view_account_details()
    elif choice == "5": train_model()
    elif choice == "6": list_my_models()
    elif choice == "7": run_live_prediction()
    elif choice == "8": logout()
    elif choice == "9": sys.exit("Terminating diagnostic session tracker.")
    else: print("❌ Invalid option selection.")


def get_headers():
    return {"Authorization": f"Bearer {session_state['token']}"} if session_state["token"] else {}


def register():
    print("\n📝 --- NEW USER REGISTER ENTRY ---")
    email = input("Enter registration email: ").strip()
    password = getpass.getpass("Enter password: ").strip()
    
    try:
        res = requests.post(f"{BASE_URL}/auth/register", json={"email": email, "password": password})
        if res.status_code == 201:
            print(f"\n✅ Account created! A custom welcome onboarding email notification was sent.")
            print(res.text)
        else:
            print(f"\n❌ Registration failed: {res.text}")
    except Exception as e:
        print(f"Connection error: {e}")


def login():
    print("\n🔐 --- SECURITY SECURE SESSION LOGIN ---")
    email = input("Enter email: ").strip()
    password = getpass.getpass("Enter password: ").strip()
    
    try:
        res = requests.post(f"{BASE_URL}/auth/login", json={"email": email, "password": password})
        if res.status_code == 200:
            data = res.json()
            session_state["user_id"] = data["user_id"]
            session_state["token"] = data["access_token"]
            print(f"\n✅ Session authenticated! Welcome back.")
        else:
            print(f"\n❌ Authentication failed: {res.text}")
    except Exception as e:
        print(f"Connection error: {e}")


def forgot_password_otp():
    print("\n🔑 --- ACCOUNT RECOVERY GATEWAY ---")
    email = input("Enter your registered account email: ").strip()
    
    try:
        print("📨 Triggering One-Time Password verification payload via secure SMTP...")
        res = requests.post(f"{BASE_URL}/auth/forgot-password", json={"email": email})
        print(f"\n📬 Status: {res.json().get('message', 'Processing done.')}")
        
        proceed = input("\nDo you want to submit your verification code and update credentials now? (y/n): ").strip().lower()
        if proceed != 'y':
            return
            
        print("\n--- CREDENTIAL CREATION INTERACTION MATRIX ---")
        otp = input("Enter 6-digit numeric OTP code received: ").strip()
        new_password = getpass.getpass("Enter New Security Password: ").strip()
        confirm_password = getpass.getpass("Confirm New Security Password: ").strip()
        
        if new_password != confirm_password:
            print("❌ Validation Error: Passwords do not match.")
            return
            
        payload = {
            "email": email,
            "otp": otp,
            "new_password": new_password
        }
        
        print("🔒 Sending system update request package...")
        reset_res = requests.post(f"{BASE_URL}/auth/reset-password-otp", json=payload)
        
        if reset_res.status_code == 200:
            print(f"\n✅ Success: {reset_res.json().get('message')}")
        else:
            print(f"\n❌ Recovery Fault: {reset_res.json().get('error', 'Token verification mismatch.')}")
            
    except Exception as e:
        print(f"Connection error: {e}")


def view_account_details():
    if not session_state["token"]:
        print("🛑 Access Denied: You must be logged in to read profile details.")
        return
        
    try:
        res = requests.get(f"{BASE_URL}/auth/me", headers=get_headers())
        if res.status_code == 200:
            profile = res.json()["user"]
            print("\n================ ACCOUNT PROFILE DETAILS ================")
            print(f"👤 System User ID Reference : {profile['id']}")
            print(f"📧 Bound Email Account     : {profile['email']}")
            print(f"📆 Registration Timestamp  : {profile['created_at']}")
            print("=========================================================\n")
        else:
            print(f"❌ Failed to fetch user profile: {res.text}")
    except Exception as e:
        print(f"Error checking profile structure: {e}")


def train_model():
    if not session_state["user_id"]:
        print("🛑 Access Denied: Log in first.")
        return
    file_path = input("Enter data file path (e.g., C:/data/weather.csv): ").strip()
    model_name = input("Assign a unique name to this model deployment: ").strip()
    target = input("Input exact target column (e.g., RainTomorrow): ").strip()
    features_list = input("Input space-separated features list: ").strip().split()

    try:
        with open(file_path, 'rb') as f:
            payload_files = {'file': f}
            payload_form = {
                'user_id': session_state["user_id"],
                'model_name': model_name,
                'targets': [target],
                'features': features_list
            }
            print("⚡ Transmission streaming sequence engaged... Training tournament live...")
            res = requests.post(f"{BASE_URL}/targets-features-train", files=payload_files, data=payload_form)
            print(res.text)
    except Exception as e:
        print(f"Error opening file: {e}")


def list_my_models():
    if not session_state["user_id"]:
        print("🛑 Access Denied: Log in first.")
        return
    
    try:
        res = requests.get(f"{BASE_URL}/developer/models", params={"user_id": session_state["user_id"]})
        if res.status_code == 200:
            models_cache = res.json()["models"]
            if not models_cache:
                print("\nℹ️ No models registered to your profile.")
                return
                
            print("\n📊 --- YOUR TRAINED AUTOMATED MODELS ENGINE SPECIFICATIONS ---")
            for idx, model in enumerate(models_cache):
                download_tag = "✅ [DOWNLOADED]" if model['has_been_downloaded'] else "🆕 [REMOTE INFRASTRUCTURE ONLY]"
                print(f"\n[{idx + 1}] Model Profile Name: {model['model_name'].upper()} (Version: v{model['model_version']})")
                print(f"    ├─ 🔍 Problem Evaluation Target Type : {model.get('problem_type', 'N/A')}")
                print(f"    ├─ 🏆 Winning Tournament Algorithm   : {model.get('algorithm_name', 'N/A')}")
                print(f"    ├─ 📈 Model Accuracy/R² Score Matrix : {model.get('performance_score', 0.0):.4f}")
                print(f"    ├─ 🎯 Ground Truth Targets Applied   : {model.get('targets', [])}")
                print(f"    ├─ 📦 Feature Vectors Parsed Array   : {model.get('features', [])}")
                print(f"    ├─ 🔑 Secure API Access Token        : {model['api_key']}")
                print(f"    └─ 💾 Storage File State Token       : {download_tag}")
            
            print("\n-----------------------------------------------------------")
            action = input("Do you want to download a model joblib binary file? (y/n): ").strip().lower()
            if action == 'y':
                item_num = int(input("Enter index number integer choice to pull down: ").strip()) - 1
                if 0 <= item_num < len(models_cache):
                    download_model_action(model_metadata=models_cache[item_num])
                else:
                    print("Invalid structural index position array chosen.")
        else:
            print(f"Could not retrieve model specifications: {res.text}")
    except Exception as e:
        print(f"Error contacting remote metadata engine registry: {e}")


def download_model_action(model_metadata):
    model_id = model_metadata["id"]
    suggested_name = f"{model_metadata['model_name'].replace(' ', '_')}_v{model_metadata['model_version']}.joblib"
    
    res = requests.get(f"{BASE_URL}/developer/models/download/{model_id}")
    if res.status_code == 200:
        root = tk.Tk()
        root.withdraw()
        root.attributes("-topmost", True)
        
        selected_file_path = filedialog.asksaveasfilename(
            initialfile=suggested_name,
            defaultextension=".joblib",
            filetypes=[("Joblib Serialized Objects", "*.joblib"), ("All Files", "*.*")],
            title="Choose Local Destination Directory to Store Model"
        )
        
        if selected_file_path:
            with open(selected_file_path, 'wb') as f:
                f.write(res.content)
            print(f"🎉 Success! Model package saved locally to:\n '{selected_file_path}'")
        else:
            print("❌ Download aborted.")
        root.destroy()
    else:
        print(f"Download stream error: {res.text}")


def run_live_prediction():
    if not session_state["user_id"]:
        print("🛑 Access Denied: Log in first.")
        return

    res = requests.get(f"{BASE_URL}/developer/models", params={"user_id": session_state["user_id"]})
    if res.status_code != 200:
        print(f"❌ Failed to retrieve models: {res.text}")
        return

    models_cache = res.json()["models"]
    if not models_cache:
        print("⚠️ No models available.")
        return

    print("\n🤖 Select a model to run inference against:")
    for idx, model in enumerate(models_cache):
        print(f"[{idx + 1}] {model['model_name'].upper()} (v{model['model_version']}) - {model.get('algorithm_name')}")

    try:
        selection = int(input("\nEnter selection number: ").strip()) - 1
        if not (0 <= selection < len(models_cache)):
            print("Invalid choice index.")
            return
    except ValueError:
        return

    selected_model = models_cache[selection]
    features_input = selected_model.get("features", [])
    if not features_input:
        features_input = input("\nEnter space-separated features manually: ").strip().split()

    payload = {}
    print(f"\n🧠 Preparing input payload structure for model: {selected_model['model_name'].upper()}")
    for feature in features_input:
        val = input(f"   Enter value for [{feature}]: ").strip()
        if val.lower() in ['null', 'none', '']:
            payload[feature] = None
        elif val.replace('.', '', 1).isdigit():
            payload[feature] = float(val) if '.' in val else int(val)
        else:
            payload[feature] = val

    print("\n⚡ Transmitting inference payload over secure API gateway...")
    headers = {"Authorization": f"Bearer {selected_model['api_key']}", "Content-Type": "application/json"}
    
    try:
        response = requests.post(f"{BASE_URL}/v1/predict", json=payload, headers=headers)
        if response.status_code == 200:
            result = response.json()
            print("\n🎯 --- INFERENCE SUCCESSFUL ---")
            print(f"    Model Used: {result['model_name']}")
            print(f"    Predicted Value Output: {result['prediction']}")
            print("--------------------------------")
        else:
            print(f"\n❌ API Gateway Rejected Request: {response.text}")
    except Exception as e:
        print(f"❌ Dispatch error: {str(e)}")


def logout():
    if not session_state["token"]:
        print("❌ You are not logged in.")
        return
    try:
        res = requests.post(f"{BASE_URL}/auth/logout", headers=get_headers())
        if res.status_code == 200:
            session_state["user_id"] = None
            session_state["token"] = None
            print("🚀 Successfully logged out. Session state cleared.")
        else:
            print(f"Logout execution failed: {res.text}")
    except Exception as e:
        print(f"Connection error: {e}")


if __name__ == "__main__":
    while True:
        main_menu()